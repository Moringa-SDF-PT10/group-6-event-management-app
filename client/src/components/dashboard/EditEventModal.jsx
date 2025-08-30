import { useEffect, useState, useContext } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { X, Calendar, Clock } from 'lucide-react';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import AuthContext from '../../context/AuthContext';

const EditEventModal = ({ isOpen, onClose, event, onEventUpdated }) => {
    const { token } = useContext(AuthContext);
    // State for the DatePicker component
    const [eventDate, setEventDate] = useState(null);
    const [eventTime, setEventTime] = useState(null);

    const formik = useFormik({
        initialValues: {
            title: '',
            description: '',
            location: '',
            venue: '',
            price: '',
            max_attendees: ''
        },
        validationSchema: Yup.object({
            title: Yup.string().required('Event name is required'),
            price: Yup.number().positive('Price must be a positive number').required('Price is required'),
            max_attendees: Yup.number().integer('Capacity must be a whole number').positive('Capacity must be positive').required('Capacity is required'),
        }),
        onSubmit: async (values) => {
            if (!eventDate || !eventTime) {
                alert("Please select a valid date and time.");
                return;
            }
            const combinedDateTime = new Date(eventDate);
            combinedDateTime.setHours(eventTime.getHours());
            combinedDateTime.setMinutes(eventTime.getMinutes());

            const updatedData = {
                ...values,
                date: combinedDateTime.toISOString(),
            };

            try {
                const response = await fetch(`http://127.0.0.1:5000/api/events/${event.id}`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(updatedData),
                });
                if (!response.ok) throw new Error('Failed to update event');
                onEventUpdated(); // Re-fetches the events list in the dashboard
                onClose();
            } catch (error) {
                alert(error.message);
            }
        },
        enableReinitialize: true,
    });

    // This effect pre-populates the form when the modal opens with a selected event
    useEffect(() => {
        if (event) {
            formik.setValues({
                title: event.title || '',
                description: event.description || '',
                location: event.location || '',
                venue: event.venue || '',
                price: event.price || '',
                max_attendees: event.max_attendees || '',
            });
            if (event.date) {
                const dateObj = new Date(event.date);
                setEventDate(dateObj);
                setEventTime(dateObj);
            }
        }
    }, [event]);

    const renderError = (field) => formik.touched[field] && formik.errors[field] && (
        <p className="text-red-500 text-xs mt-1">{formik.errors[field]}</p>
    );

    if (!isOpen) return null;

    return (
        <AnimatePresence>
            <motion.div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm" onClick={onClose}>
                <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    exit={{ scale: 0.9, opacity: 0 }}
                    className="bg-white rounded-xl shadow-2xl w-full max-w-2xl"
                    onClick={(e) => e.stopPropagation()}
                >
                    <div className="p-6 border-b flex justify-between items-center">
                        <h2 className="text-2xl font-bold text-charcoal">Edit Event: {event?.title}</h2>
                        <button onClick={onClose} className="p-2 rounded-full hover:bg-gray-100"><X size={20} /></button>
                    </div>
                    <form onSubmit={formik.handleSubmit} className="p-6 space-y-4 max-h-[80vh] overflow-y-auto">
                        <div>
                            <label className="font-semibold text-sm">Event Title</label>
                            <input name="title" {...formik.getFieldProps('title')} className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
                            {renderError('title')}
                        </div>
                        <div>
                            <label className="font-semibold text-sm">Event Description</label>
                            <textarea name="description" {...formik.getFieldProps('description')} rows="3" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md"></textarea>
                        </div>
                         <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="font-semibold text-sm">Location</label>
                                <input name="location" {...formik.getFieldProps('location')} className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
                            </div>
                            <div>
                                <label className="font-semibold text-sm">Venue</label>
                                <input name="venue" {...formik.getFieldProps('venue')} className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
                            </div>
                        </div>
                         <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="font-semibold text-sm">Date</label>
                                <div className="relative mt-1">
                                    <Calendar size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
                                    <DatePicker selected={eventDate} onChange={(date) => setEventDate(date)} dateFormat="dd/MM/yyyy" placeholderText="Select date" className="w-full pl-10 pr-3 py-3 bg-gray-50 border border-gray-200 rounded-lg"/>
                                </div>
                            </div>
                            <div>
                                <label className="font-semibold text-sm">Time</label>
                                <div className="relative mt-1">
                                    <Clock size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"/>
                                    <DatePicker selected={eventTime} onChange={(time) => setEventTime(time)} showTimeSelect showTimeSelectOnly timeIntervals={15} timeCaption="Time" dateFormat="h:mm aa" placeholderText="Select time" className="w-full pl-10 pr-3 py-3 bg-gray-50 border border-gray-200 rounded-lg"/>
                                </div>
                            </div>
                        </div>
                         <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="font-semibold text-sm">Ticket Price (KES)</label>
                                <input name="price" type="number" {...formik.getFieldProps('price')} className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
                                {renderError('price')}
                            </div>
                            <div>
                                <label className="font-semibold text-sm">Capacity</label>
                                <input name="max_attendees" type="number" {...formik.getFieldProps('max_attendees')} className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
                                {renderError('max_attendees')}
                            </div>
                        </div>
                        <div className="pt-4 flex justify-end gap-2">
                            <button type="button" onClick={onClose} className="px-4 py-2 text-sm font-semibold rounded-md text-charcoal hover:bg-gray-100">Cancel</button>
                            <button type="submit" className="px-4 py-2 text-sm font-semibold bg-coral text-white rounded-md hover:bg-opacity-90">Save Changes</button>
                        </div>
                    </form>
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};

export default EditEventModal;

