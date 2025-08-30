import { useState, useContext } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Ticket, CheckCircle, Plus, Minus } from 'lucide-react';
import AuthContext from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const PurchaseTicketModal = ({ isOpen, onClose, event }) => {
    const { token } = useContext(AuthContext);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [isSuccess, setIsSuccess] = useState(false);
    const navigate = useNavigate();
    
    // State and handlers for ticket quantity 
    const [quantity, setQuantity] = useState(1);

    const handleDecrement = () => {
        setQuantity(prev => (prev > 1 ? prev - 1 : 1));
    };

    const handleIncrement = () => {
        setQuantity(prev => prev + 1);
    };

    const totalPrice = (event?.price * quantity).toLocaleString();


    const handleConfirmPurchase = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await fetch('http://127.0.0.1:5000/api/tickets/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                // Send quantity in the request body 
                body: JSON.stringify({ event_id: event.id, quantity: quantity })
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Failed to purchase ticket.');
            }
            setIsSuccess(true);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleClose = () => {
        setIsSuccess(false);
        setError(null);
        setQuantity(1); // Resets quantity on close
        onClose();
    };

    const handleViewTickets = () => {
        handleClose();
        navigate('/dashboard');
    };

    if (!isOpen || !event) return null;

    return (
        <AnimatePresence>
             <motion.div
                className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm"
                onClick={handleClose}
            >
                <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    exit={{ scale: 0.9, opacity: 0 }}
                    className="bg-white rounded-xl shadow-2xl w-full max-w-md p-6"
                    onClick={(e) => e.stopPropagation()}
                >
                    {isSuccess ? (
                        <div className="text-center">
                            <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
                            <h3 className="text-2xl font-bold text-charcoal">Purchase Successful!</h3>
                            <p className="text-slate-light mt-2">You've got {quantity} ticket(s) for "{event.title}". See you there!</p>
                             <div className="mt-6 flex justify-center gap-3">
                                <button onClick={handleClose} className="px-4 py-2 font-semibold rounded-md text-charcoal hover:bg-gray-100">Close</button>
                                <button onClick={handleViewTickets} className="px-4 py-2 font-semibold bg-coral text-white rounded-md hover:bg-opacity-90">View My Tickets</button>
                            </div>
                        </div>
                    ) : (
                        <>
                            <div className="text-center">
                                <Ticket className="h-12 w-12 text-coral mx-auto mb-4" />
                                <h3 className="text-lg leading-6 font-bold text-charcoal">Confirm Your Tickets</h3>
                                <div className="mt-4 text-left bg-gray-50 p-4 rounded-lg space-y-3">
                                    <div>
                                        <p className="font-bold text-charcoal">{event.title}</p>
                                        <p className="text-sm text-slate-light">{new Date(event.date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}</p>
                                    </div>
                                    {/* Quantity Selector UI */}
                                    <div className="flex justify-between items-center">
                                        <p className="font-semibold text-slate-light">Quantity</p>
                                        <div className="flex items-center gap-2">
                                            <button onClick={handleDecrement} className="p-1.5 rounded-full bg-gray-200 hover:bg-gray-300"><Minus size={16} /></button>
                                            <span className="font-bold text-lg w-8 text-center">{quantity}</span>
                                            <button onClick={handleIncrement} className="p-1.5 rounded-full bg-gray-200 hover:bg-gray-300"><Plus size={16} /></button>
                                        </div>
                                    </div>
                                    {/* Total Price Display */}
                                    <div className="flex justify-between items-center border-t pt-3">
                                        <p className="font-bold text-charcoal">Total Price</p>
                                        <p className="text-lg font-bold text-coral">{event.price > 0 ? `KES ${totalPrice}` : 'Free'}</p>
                                    </div>
                                </div>
                                {error && <p className="text-red-500 text-sm mt-4 text-center">{error}</p>}
                            </div>
                            <div className="mt-6 flex justify-end gap-3">
                                <button type="button" onClick={handleClose} className="px-4 py-2 text-sm font-semibold rounded-md text-charcoal hover:bg-gray-100">Cancel</button>
                                <button
                                    type="button"
                                    onClick={handleConfirmPurchase}
                                    disabled={isLoading}
                                    className="px-4 py-2 text-sm font-semibold bg-coral text-white rounded-md hover:bg-opacity-90 disabled:bg-gray-400"
                                >
                                    {isLoading ? 'Processing...' : 'Confirm Purchase'}
                                </button>
                            </div>
                        </>
                    )}
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};

export default PurchaseTicketModal;