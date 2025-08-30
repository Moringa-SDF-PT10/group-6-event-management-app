import { useState, useContext, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, UploadCloud, Calendar, Clock } from "lucide-react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import AuthContext from "../../context/AuthContext";

// --- ADDED: Expanded list of accepted image formats ---
const ACCEPTED_IMAGE_TYPES = "image/jpeg, image/jpg, image/png, image/webp, image/heic";
const ACCEPTED_IMAGE_MIMES = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/heic"];

const CreateEventModal = ({ isOpen, onClose, onEventCreated }) => {
  const { token } = useContext(AuthContext);
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [eventDate, setEventDate] = useState(null);
  const [eventTime, setEventTime] = useState(null);
  const fileInputRef = useRef(null);

  const [formData, setFormData] = useState({
    title: "",
    description: "",
    location: "",
    venue: "",
    price: "",
    max_attendees: "",
  });

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    // --- UPDATED: Check against the new list of mime types ---
    if (file && ACCEPTED_IMAGE_MIMES.includes(file.type)) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    } else {
      setImageFile(null);
      setImagePreview(null);
      alert("Please upload a valid image file (JPG, PNG, WEBP, HEIC).");
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleDropzoneClick = () => {
    fileInputRef.current.click();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!eventDate || !eventTime) {
        alert("Please select a date and time for the event.");
        return;
    }

    const combinedDateTime = new Date(eventDate);
    combinedDateTime.setHours(eventTime.getHours());
    combinedDateTime.setMinutes(eventTime.getMinutes());

    const dataToSend = new FormData();
    Object.keys(formData).forEach(key => dataToSend.append(key, formData[key]));
    dataToSend.append("date", combinedDateTime.toISOString());
    if (imageFile) {
      dataToSend.append("image_url", imageFile); 
    }
    
    try {
      // UPDATED: Changed to a relative path
      const response = await fetch("/api/events/", {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: dataToSend,
      });
      
      const responseData = await response.json();
      if (!response.ok) {
        throw new Error(responseData.error || "Failed to create event.");
      }

      onEventCreated();
      onClose();

    } catch (error) {
      console.error("Error creating event:", error);
      alert(error.message);
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, y: 50, opacity: 0 }}
          animate={{ scale: 1, y: 0, opacity: 1 }}
          exit={{ scale: 0.9, y: 50, opacity: 0 }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
          className="bg-white rounded-xl shadow-2xl w-full max-w-2xl"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="p-6 border-b flex justify-between items-center">
            <h2 className="text-2xl font-bold text-charcoal">Create a New Event</h2>
            <button onClick={onClose} className="p-2 rounded-full hover:bg-gray-100"><X size={20} /></button>
          </div>

          <form onSubmit={handleSubmit} className="p-6 space-y-4 max-h-[80vh] overflow-y-auto">
            <div>
              <label className="font-semibold text-sm mb-1 block">Event Banner</label>
              <input
                  type="file"
                  ref={fileInputRef}
                  className="hidden"
                  // --- UPDATED: Use the new accept string ---
                  accept={ACCEPTED_IMAGE_TYPES}
                  onChange={handleFileChange}
              />
              <div
                className="w-full h-48 border-2 border-dashed rounded-lg flex flex-col items-center justify-center text-center cursor-pointer hover:bg-gray-50 transition-colors bg-cover bg-center"
                style={{ backgroundImage: `url(${imagePreview})` }}
                onClick={handleDropzoneClick}
              >
                {!imagePreview && (
                    <>
                      <UploadCloud size={40} className="text-gray-400 mb-2" />
                      <p className="text-charcoal font-semibold">Click to upload or drag and drop</p>
                      <p className="text-xs text-slate-light">JPG, PNG, WEBP, HEIC</p>
                    </>
                )}
              </div>
            </div>

            {/* Other form fields remain the same */}
            <div>
              <label className="font-semibold text-sm">Event Title</label>
              <input type="text" name="title" value={formData.title} onChange={handleInputChange} placeholder="e.g., Nairobi Tech Summit" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md"/>
            </div>

            <div>
              <label className="font-semibold text-sm">Event Description</label>
              <textarea name="description" value={formData.description} onChange={handleInputChange} placeholder="Tell us about your event..." rows="3" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md"></textarea>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
               <div>
                <label className="font-semibold text-sm">Location</label>
                <input name="location" value={formData.location} onChange={handleInputChange} placeholder="e.g., Nairobi" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md"/>
              </div>
              <div>
                <label className="font-semibold text-sm">Venue</label>
                <input name="venue" value={formData.venue} onChange={handleInputChange} placeholder="e.g., KICC" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
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
                <input type="number" name="price" value={formData.price} onChange={handleInputChange} placeholder="e.g., 1500" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
              </div>
              <div>
                <label className="font-semibold text-sm">Capacity</label>
                <input type="number" name="max_attendees" value={formData.max_attendees} onChange={handleInputChange} placeholder="e.g., 200" className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md" />
              </div>
            </div>

            <div className="pt-4 flex justify-end gap-2">
              <button type="button" onClick={onClose} className="px-4 py-2 text-sm font-semibold rounded-md text-charcoal hover:bg-gray-100">Cancel</button>
              <button type="submit" className="px-4 py-2 text-sm font-semibold bg-coral text-white rounded-md hover:bg-opacity-90">Create Event</button>
            </div>
          </form>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default CreateEventModal;
