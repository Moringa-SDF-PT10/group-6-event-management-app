import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { X, Calendar, Clock } from 'lucide-react';

const EditEventModal = ({ isOpen, onClose, event }) => {
    const formik = useFormik({
        initialValues: {
            eventName: '',
            description: '',
            date: '',
            time: '',
            price: '',
            capacity: ''
        },
        validationSchema: Yup.object({
            eventName: Yup.string().required('Event name is required'),
            date: Yup.date().required('Date is required').min(new Date(), 'Date must be in the future'),
            price: Yup.number().positive('Price must be a positive number').required('Price is required'),
            capacity: Yup.number().integer('Capacity must be a whole number').positive('Capacity must be positive').required('Capacity is required'),
        }),
        onSubmit: (values) => {
            alert('Submitting updated event data (see console)');
            console.log({ eventId: event.id, ...values });
            onClose();
        },
        enableReinitialize: true, // This is important to update the form when the event prop changes
    });

    // This effect pre-populates the form when the modal opens with a selected event
    useEffect(() => {
        if (event) {
            formik.setValues({
                eventName: event.title || '',
                description: event.description || '',
                date: event.date || '',
                time: event.time || '',
                price: event.price || '',
                capacity: event.capacity || '',
            });
        }
    }, [event]);

    const renderError = (field) => formik.touched[field] && formik.errors[field] && (
        <p className="text-red-500 text-xs mt-1">{formik.errors[field]}</p>
    );

    if (!isOpen) return null;

    return (
        <AnimatePresence>
            <motion.div
                className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm"
                onClick={onClose}
            >
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
                    {/* UPDATED: The full form is now here */}
                    <form onSubmit={formik.handleSubmit} className="p-6 space-y-4 max-h-[80vh] overflow-y-auto">
                        <div>
                            <label className="font-semibold text-sm">Event Name</label>
                            <input name="eventName" {...formik.getFieldProps('eventName')} placeholder="e.g., Nairobi Tech Summit" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
                            {renderError('eventName')}
                        </div>
                        <div>
                            <label className="font-semibold text-sm">Event Description</label>
                            <textarea name="description" {...formik.getFieldProps('description')} placeholder="Tell us about your event..." rows="3" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md"></textarea>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="relative">
                                <label className="font-semibold text-sm">Date</label>
                                <Calendar size={18} className="absolute left-3 top-10 text-gray-400 pointer-events-none" />
                                <input name="date" type="date" {...formik.getFieldProps('date')} className="w-full mt-1 p-3 pl-10 bg-gray-100 border border-gray-200 rounded-md" />
                                {renderError('date')}
                            </div>
                            <div className="relative">
                                <label className="font-semibold text-sm">Time</label>
                                <Clock size={18} className="absolute left-3 top-10 text-gray-400 pointer-events-none" />
                                <input name="time" type="time" {...formik.getFieldProps('time')} className="w-full mt-1 p-3 pl-10 bg-gray-100 border border-gray-200 rounded-md" />
                            </div>
                        </div>
                         <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="font-semibold text-sm">Ticket Price (KES)</label>
                                <input name="price" type="number" {...formik.getFieldProps('price')} placeholder="e.g., 1500" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
                                {renderError('price')}
                            </div>
                            <div>
                                <label className="font-semibold text-sm">Capacity</label>
                                <input name="capacity" type="number" {...formik.getFieldProps('capacity')} placeholder="e.g., 200" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
                                {renderError('capacity')}
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