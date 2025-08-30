import { useState, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import DashboardHeader from '../components/dashboard/DashboardHeader';
import CreateEventModal from '../components/dashboard/CreateEventModal';
import { AttendeeDashboardLayout } from '../components/dashboard/AttendeeComponents';
import { OrganizerDashboardLayout } from '../components/dashboard/OrganizerComponents';

const DashboardPage = () => {
    const { user } = useContext(AuthContext);
    const [isCreateModalOpen, setCreateModalOpen] = useState(false);
    const [refreshTrigger, setRefreshTrigger] = useState(0);
    const handleEventCreated = () => {
        setCreateModalOpen(false);
        setRefreshTrigger(prev => prev + 1); 
    };

    if (!user) {
        return <div className="min-h-screen bg-cream flex items-center justify-center">Loading...</div>;
    }

    const isOrganizer = user.role === 'organizer';

    return (
        <div className="min-h-screen bg-gray-100 font-sans">
            {/* The Create Event Modal with the onEventCreated prop */}
            {isOrganizer && (
                <CreateEventModal 
                    isOpen={isCreateModalOpen} 
                    onClose={() => setCreateModalOpen(false)} 
                    onEventCreated={handleEventCreated} 
                />
            )}
            
            <DashboardHeader user={user} />
            
            <main className="p-6 container mx-auto">
                {isOrganizer ? (
                    <OrganizerDashboardLayout 
                        onCreateEvent={() => setCreateModalOpen(true)}
                        refreshTrigger={refreshTrigger}
                    />
                ) : (
                    <AttendeeDashboardLayout />
                )}
            </main>
        </div>
    );
};

export default DashboardPage;