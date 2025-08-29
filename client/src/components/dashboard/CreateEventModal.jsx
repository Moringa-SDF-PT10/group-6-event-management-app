import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, UploadCloud, Calendar, Clock } from "lucide-react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const CreateEventModal = ({ isOpen, onClose }) => {
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [eventDate, setEventDate] = useState(null);
  const [eventTime, setEventTime] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    description: "",
    price: "",
    capacity: "",
  });

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && ["image/jpeg", "image/png", "image/jpg"].includes(file.type)) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    } else {
      setImagePreview(null);
      alert("Please upload a valid image file (JPG, PNG).");
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const { name, description, price, capacity } = formData;
    const eventDateTime = new Date(eventDate);
    if (eventTime) {
      eventDateTime.setHours(eventTime.getHours());
      eventDateTime.setMinutes(eventTime.getMinutes());
    }

    // Use FormData to send both text and file data
    const dataToSend = new FormData();
    dataToSend.append("name", name);
    dataToSend.append("description", description);
    dataToSend.append("date", eventDateTime.toISOString());
    dataToSend.append("price", price);
    dataToSend.append("capacity", capacity);
    if (imageFile) {
      dataToSend.append("banner_image", imageFile);
    }
    
    // Get the auth token from localStorage
    const token = localStorage.getItem("token");

    try {
  const response = await fetch("http://your-api-url.com/api/events", {
    method: "POST",
    headers: {
      "x-auth-token": token,
    },
    body: dataToSend,
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || "Failed to create event.");
  }

  const createdEvent = await response.json();
  console.log("Event created successfully:", createdEvent);
  onClose();

} catch (error) {
  console.error("Error creating event:", error);
  alert(error.message);
}
  }
  

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
          {/* Header */}
          <div className="p-6 border-b flex justify-between items-center">
            <h2 className="text-2xl font-bold text-charcoal">
              Create a New Event
            </h2>
            <button
              onClick={onClose}
              className="p-2 rounded-full hover:bg-gray-100"
            >
              <X size={20} />
            </button>
          </div>

          {/* Form */}
          <form className="p-6 space-y-4 max-h-[80vh] overflow-y-auto">
            {/* Event Banner Upload */}
            <div>
              <label className="font-semibold text-sm mb-1 block">
                Event Banner
              </label>
              <div className="relative w-full h-48">
                <div
                  className="w-full h-full border-2 border-dashed rounded-lg flex flex-col items-center justify-center text-center cursor-pointer hover:bg-gray-50 transition-colors bg-cover bg-center"
                  style={{ backgroundImage: `url(${imagePreview})` }}
                >
                  {!imagePreview && (
                    <>
                      <UploadCloud
                        size={40}
                        className="text-gray-400 mb-2"
                      />
                      <p className="text-charcoal font-semibold">
                        Click to upload or drag and drop
                      </p>
                      <p className="text-xs text-slate-light">
                        PNG, JPG, or JPEG
                      </p>
                    </>
                  )}
                </div>
                <input
                  type="file"
                  className="opacity-0 absolute inset-0 w-full h-full cursor-pointer"
                  accept="image/png, image/jpeg, image/jpg"
                  onChange={handleFileChange}
                />
              </div>
            </div>

            {/* Event Name */}
            <div>
              <label className="font-semibold text-sm">Event Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="e.g., Nairobi Tech Summit"
                className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md"
              />
            </div>

            {/* Description */}
            <div>
              <label className="font-semibold text-sm">Event Description</label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Tell us about your event..."
                rows="3"
                className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md"
              ></textarea>
            </div>

            {/* Date + Time (React Datepicker) */}
            <div className="grid grid-cols-2 gap-4">
              {/* Date Picker */}
              <div>
                <label className="font-semibold text-sm">Date</label>
                <div className="relative mt-1">
                  <Calendar
                    size={18}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"
                  />
                  <DatePicker
                    selected={eventDate}
                    onChange={(date) => setEventDate(date)}
                    dateFormat="dd/MM/yyyy"
                    placeholderText="Select date"
                    className="w-full pl-10 pr-3 py-3 bg-gray-50 border border-gray-200 rounded-lg shadow-sm focus:border-coral focus:ring-2 focus:ring-coral/40 transition-all"
                  />
                </div>
              </div>

              {/* Time Picker */}
              <div>
                <label className="font-semibold text-sm">Time</label>
                <div className="relative mt-1">
                  <Clock
                    size={18}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"
                  />
                  <DatePicker
                    selected={eventTime}
                    onChange={(time) => setEventTime(time)}
                    showTimeSelect
                    showTimeSelectOnly
                    timeIntervals={15}
                    timeCaption="Time"
                    dateFormat="h:mm aa"
                    placeholderText="Select time"
                    className="w-full pl-10 pr-3 py-3 bg-gray-50 border border-gray-200 rounded-lg shadow-sm focus:border-coral focus:ring-2 focus:ring-coral/40 transition-all"
                  />
                </div>
              </div>
            </div>

            {/* Price + Capacity */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="font-semibold text-sm">
                  Ticket Price (KES)
                </label>
                <input
                  type="number"
                  name="price"
                  value={formData.price}
                  onChange={handleInputChange}
                  placeholder="e.g., 1500"
                  className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md"
                />
              </div>
              <div>
                <label className="font-semibold text-sm">Capacity</label>
                <input
                  type="number"
                  name="capacity"
                  value={formData.capacity}
                  onChange={handleInputChange}
                  placeholder="e.g., 200"
                  className="w-full mt-1 p-3 bg-gray-100 border border-gray-200 rounded-md"
                />
              </div>
            </div>

            {/* Buttons */}
            <div className="pt-4 flex justify-end gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-sm font-semibold rounded-md text-charcoal hover:bg-gray-100"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 text-sm font-semibold bg-coral text-white rounded-md hover:bg-opacity-90"
              >
                Create Event
              </button>
            </div>
          </form>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default CreateEventModal;
