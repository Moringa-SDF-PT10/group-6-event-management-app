import { useContext } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import AuthContext from '../../context/AuthContext';
import { User, Mail, Phone, Lock, FileText } from 'lucide-react';

// A small reusable component for our input fields
const InputWithIcon = ({ icon, name, placeholder, type = 'text', formik }) => {
    const Icon = icon;
    const hasError = formik.touched[name] && formik.errors[name];
    
    return (
        <div className="relative">
            <Icon 
                className={`absolute left-3 top-1/2 -translate-y-1/2 ${hasError ? 'text-red-500' : 'text-gray-400'}`} 
                size={20} 
            />
            <input 
                name={name} 
                placeholder={placeholder}
                type={type}
                onChange={formik.handleChange}
                value={formik.values[name]}
                className={`w-full pl-10 pr-4 py-3 bg-gray-100 rounded-md border ${hasError ? 'border-red-500' : 'border-gray-200'} focus:outline-none focus:ring-2 focus:ring-coral/50`}
            />
        </div>
    );
};


const AuthForm = ({ isLogin, setIsLogin, role }) => {
    const { login, signup } = useContext(AuthContext);

    const loginSchema = Yup.object().shape({
        username: Yup.string().required('Username is required'),
        password: Yup.string().required('Password is required'),
    });

    const signupSchema = Yup.object().shape({
        firstName: Yup.string().required('First name is required'),
        lastName: Yup.string().required('Last name is required'),
        phoneNumber: Yup.string().required('Phone number is required'),
        email: Yup.string().email('Invalid email').required('Email is required'),
        username: Yup.string().required('Username is required'),
        password: Yup.string().min(8, 'Password must be at least 8 characters').required('Password is required'),
        confirmPassword: Yup.string().oneOf([Yup.ref('password'), null], 'Passwords must match').required('Confirm Password is required'),
        terms: Yup.boolean().oneOf([true], 'You must accept the terms and conditions'),
    });

    const formik = useFormik({
        initialValues: {
            firstName: '',
            lastName: '',
            phoneNumber: '',
            email: '',
            username: '',
            password: '',
            confirmPassword: '',
            terms: false,
            role: role,
        },
        validationSchema: isLogin ? loginSchema : signupSchema,
        onSubmit: (values) => {
            if (isLogin) {
                login(values);
            } else {
                signup({ ...values, role });
            }
        },
        enableReinitialize: true, 
    });

    const renderError = (field) => formik.touched[field] && formik.errors[field] && (
        <p className="text-red-500 text-xs mt-1">{formik.errors[field]}</p>
    );

    return (
        <div>
            <h2 className="text-3xl font-bold text-center text-charcoal mb-6">
                {isLogin ? 'Log In' : 'Create Your Account'}
            </h2>
            <form onSubmit={formik.handleSubmit} className="space-y-4">
                {!isLogin && (
                    <>
                        <div className="flex gap-4">
                            <div className="w-1/2">
                                <InputWithIcon icon={User} name="firstName" placeholder="First Name" formik={formik} />
                                {renderError('firstName')}
                            </div>
                            <div className="w-1/2">
                                <InputWithIcon icon={User} name="lastName" placeholder="Last Name" formik={formik} />
                                {renderError('lastName')}
                            </div>
                        </div>
                        <InputWithIcon icon={Phone} name="phoneNumber" placeholder="Phone Number" formik={formik} />
                        {renderError('phoneNumber')}
                        <InputWithIcon icon={Mail} name="email" placeholder="Email Address" type="email" formik={formik} />
                        {renderError('email')}
                    </>
                )}
                <InputWithIcon icon={User} name="username" placeholder="Username" formik={formik} />
                {renderError('username')}
                <InputWithIcon icon={Lock} name="password" placeholder="Password" type="password" formik={formik} />
                {renderError('password')}
                {!isLogin && (
                    <>
                        <InputWithIcon icon={Lock} name="confirmPassword" placeholder="Confirm Password" type="password" formik={formik} />
                        {renderError('confirmPassword')}
                        <div className="flex items-center">
                            <input name="terms" type="checkbox" onChange={formik.handleChange} checked={formik.values.terms} className="h-4 w-4 rounded border-gray-300 text-coral focus:ring-coral" />
                            <label className="ml-2 text-sm text-slate-light">I agree to the <a href="#" className="font-semibold text-coral hover:underline">Terms and Conditions</a></label>
                        </div>
                        {renderError('terms')}
                    </>
                )}
                <button type="submit" className="w-full py-3 font-semibold text-white bg-coral rounded-md hover:bg-opacity-90 transition-colors">
                    {isLogin ? 'Log In' : 'Register'}
                </button>
            </form>
            <p className="text-sm text-center text-slate-light mt-6">
                {isLogin ? "Don't have an account?" : 'Already have an account?'}
                <button onClick={() => setIsLogin(!isLogin)} className="font-semibold text-coral hover:underline ml-1">
                    {isLogin ? 'Sign Up' : 'Log In'}
                </button>
            </p>
        </div>
    );
};

export default AuthForm;
