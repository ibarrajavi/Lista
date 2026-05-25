import { Link } from 'react-router-dom'

function Login() {
    return (
<section className="bg-bg ">
  <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      <div className="w-full bg-elev rounded-card shadow dark:border md:mt-0 sm:max-w-md xl:p-0">
          <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
            
            {/* Card title */}
            <div className='justify-self-center justify-items-center text-center'>
              <Link 
                to="/"
                className="self-center font-serif italic font-normal text-3xl">
                  Lista
              </Link>
              <h2 className='self-center font-serif italic font-normal text-xl mt-3 py-1.5'> 
                Welcome back
              </h2>
              <h4 className="text-sm font-sans text-ink-muted"> 
                Sign in to your Listas.
              </h4>
              </div>


              <form className="space-y-4 md:space-y-6" action="#">
                {/* Username or email */}
                  <div>
                      <label htmlFor="email" className="block mb-2 text-sm font-sans text-ink-muted">Username or email</label>
                      <input type="email" name="email" id="email" className="bg-gray-50 border border-gray-300 text-sm font-sans rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5" placeholder="name or name@company.com" required/>
                  </div>

                {/* Password */}
                  <div>
                      <label htmlFor="password" className="block mb-2 text-sm font-sans text-ink-muted">Password</label>
                      <input type="password" name="password" id="password" placeholder="••••••••" className="bg-gray-50 border border-gray-300 text-sm font-sans rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5" required/>
                  </div>

                {/* Login button */}
                  <button type="submit" className="font-sans text-[13px] font-normal bg-[#161514] text-[#FFFFFF] py-2 px-[14px] rounded-ctrl rounded-[8px] cursor-pointer w-full hover:bg-primary-700 px-5 py-2.5 text-center hover:bg-[#6B6963]">Log in</button>
                  <p className="text-sm font-sans text-ink-muted justify-self-center justify-items-center text-center">
                      Don’t have an account? <a href="#" className="font-medium text-primary-600 hover:underline">Register</a>
                  </p>
              </form>
          </div>
      </div>
  </div>
</section>
    );
}

export default Login;