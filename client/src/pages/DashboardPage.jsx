import { useState, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import DashboardHeader from '../components/dashboard/DashboardHeader';
import CreateEventModal from '../components/dashboard/CreateEventModal';
import { AttendeeDashboardLayout } from '../components/dashboard/AttendeeComponents';
import { OrganizerDashboardLayout } from '../components/dashboard/OrganizerComponents';

const DashboardPage = () => {
    const { user } = useContext(AuthContext);
    const [isCreateModalOpen, setCreateModalOpen] = useState(false);

    if (!user) {
        return <div className="min-h-screen bg-cream flex items-center justify-center">Loading...</div>;
    }

    const isOrganizer = user.role === 'organizer';

    return (
        <div className="min-h-screen bg-gray-100 font-sans">
            {/* The Create Event Modal, only available to organizers */}
            {isOrganizer && <CreateEventModal isOpen={isCreateModalOpen} onClose={() => setCreateModalOpen(false)} />}
            
            <DashboardHeader user={user} />
            
            <main className="p-6 container mx-auto">
                {isOrganizer ? (
                    <OrganizerDashboardLayout onCreateEvent={() => setCreateModalOpen(true)} />
                ) : (
                    <AttendeeDashboardLayout />
                )}
            </main>
        </div>
    );
};

export default DashboardPage;