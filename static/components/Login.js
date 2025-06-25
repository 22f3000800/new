export default{
    template : `
    <div class = "row border">
        <div class = "col" style ="height: 750px;">
            <div class = "border mx-auto mt-5" style ="height: 400px;width : 300px">
                <div>
                    <h2 class="text-center"> Login</h2>
                    <div class="mx-2 mb-3">
                        <label for="email" class="form-label">Email address</label>
                        <input type="email" class="form-control" id="email" v-model="formData.email" placeholder="name@example.com">
                    </div>
                    <div class="mx-2 mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" v-model="formData.password">
                    </div>
                    <div class="mx-2 mb-3 text-center">
                        <button class="btn btn-primary" @click="loginUser"> Login</button>
                    </div>
                    <!-- IMPORTANT: Add this div to display messages -->
                    <div v-if="message" :class="messageClass" class="mt-3">
                        {{ message }}
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
    data:function(){
        return{
            formData:{ // Here formData is a single object that takes both email and password
                email : "",
                password : ""
            },
            message: "", // For displaying messages from the server
            messageClass: "" // For styling messages (e.g., text-success, text-danger)
        } 
    },
    methods:{
        loginUser: function() {
            this.message = ""; // Clear previous messages
            this.messageClass = "";

            // Optional: Basic client-side validation
            if (!this.formData.email || !this.formData.password) {
                this.message = "Email and password are required!";
                this.messageClass = "text-danger";
                return;
            }

            console.log("Sending data:", this.formData); // Debugging: See what's being sent

            fetch('/api/login', {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(this.formData)
            })
            .then(response => {
                // Check if the response was successful (HTTP status 200-299)
                if (response.ok) {
                    return response.json(); 
                } else {
                    // For non-2xx responses, parse the JSON error body
                    return response.json().then(errorData => {
                        // Throw an error with the server's message or a default
                        throw new Error(errorData.message || 'Login failed on server.');
                    });
                }
            })
            .then(data => {
                console.log("Login response:", data);
                
                // Check for the 'auth-token' to determine successful login
                if (data["auth-token"]) {
                    // Store auth token and user info in localStorage
                    localStorage.setItem("auth-token", data["auth-token"]);
                    localStorage.setItem("user-id", data.id); 
                    localStorage.setItem("username", data.username); 
                    // IMPORTANT: Store roles received from the backend
                    localStorage.setItem("user-roles", JSON.stringify(data.roles)); 

                    this.message = data.message || "Login successful!"; // Display success message from backend
                    this.messageClass = "text-success";

                    // --- Role-based Redirection Logic ---
                    if (data.roles.includes('admin')) {
                        this.$router.push('/admin-dashboard'); // Redirect admin users like redirect('/admin_dashboard')
                    } else if (data.roles && data.roles.includes('user')) {
                        this.$router.push('/user-dashboard'); // Redirect regular users
                    } else {
                        // Default redirect if no specific role or unknown role
                        this.message = "Login successful, but no specific dashboard for your role. Redirecting to home.";
                        this.messageClass = "text-info"; // A neutral info message
                        this.$router.push('/'); 
                    }
                    // --- End Role-based Redirection Logic ---

                } else {
                    this.message = data.message || "Login failed: Missing authentication token.";
                    this.messageClass = "text-danger";
                }
            })
            .catch(error => {
                // This catches network errors or errors thrown from the .then() block
                console.error("Login error:", error);
                this.message = error.message || "Network error or server unreachable. Please try again.";
                this.messageClass = "text-danger";
            });
        }
    }
}





/*
export default{
    template : `
    <div class = "row border">
        <div class = "col" style ="height: 750px;">
            <div class = "border mx-auto mt-5" style ="height: 400px;width : 300px">
                <div>
                    <h2 class="text-center"> Login</h2>
                    <div>
                        <label for="email">Enter your email</label>
                        <input type="text" id="email" v-model="formData.email" class="form-control">
                    </div>
                    <div class="mt-3">
                        <label for="pass">Enter your password</label>
                        <input type="password" id="pass" v-model="formData.password" class="form-control">
                    </div>
                    <div class="mt-4">
                        <button class="btn btn-primary" @click="loginUser"> Login</button>
                    </div>
                    <!-- IMPORTANT: Add this div to display messages -->
                    <div v-if="message" :class="messageClass" class="mt-3">
                        {{ message }}
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
    data:function(){
        return{
            formData:{ // Here formData is a single object that takes both email and password
                email : "",
                password : ""
            },
            message: "", // For displaying messages from the server
            messageClass: "" // For styling messages (e.g., text-success, text-danger)
        } 
    },
    methods:{
        loginUser: function() {
            this.message = ""; // Clear previous messages
            this.messageClass = "";

            // Optional: Basic client-side validation
            if (!this.formData.email || !this.formData.password) {
                this.message = "Email and password are required!";
                this.messageClass = "text-danger";
                return;
            }

            console.log("Sending login data:", this.formData); // Debugging: See what's being sent

            fetch('/api/login', {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(this.formData)
            })
            .then(response => {
                // Check if the response was successful (HTTP status 200-299)
                if (response.ok) {
                    return response.json(); 
                } else {
                    // For non-2xx responses, parse the JSON error body
                    return response.json().then(errorData => {
                        // Throw an error with the server's message or a default
                        throw new Error(errorData.message || 'Login failed on server.');
                    });
                }
            })
            .then(data => {
                console.log("Login response:", data);
                
                // Check for the 'auth-token' to determine successful login
                if (data["auth-token"]) {
                    // Store auth token and user info in localStorage
                    localStorage.setItem("auth-token", data["auth-token"]);
                    localStorage.setItem("user-id", data.id); // Store user ID
                    localStorage.setItem("username", data.username); // Store username
                    // IMPORTANT: Store roles received from the backend
                    localStorage.setItem("user-roles", JSON.stringify(data.roles));

                    this.message = data.message || "Login successful!"; // Display success message from backend
                    this.messageClass = "text-success";

                    // Use Vue Router for navigation to avoid full page reload
                    // Redirect to the dashboard after successful login
                    // --- Role-based Redirection Logic ---
                    if (data.roles && data.roles.includes('admin')) {
                        this.$router.push('/admin-dashboard'); // Redirect admin users
                    } else if (data.roles && data.roles.includes('user')) {
                        this.$router.push('/user-dashboard'); // Redirect regular users
                    } else {
                        // Default redirect if no specific role or unknown role
                        this.message = "Login successful, but no specific dashboard for your role. Redirecting to home.";
                        this.messageClass = "text-info"; // A neutral info message
                        this.$router.push('/');
                   
                } else {
                    // This 'else' block would catch cases where backend sends 200 OK but no token (unlikely with our backend)
                    this.message = data.message || "Login failed: Missing authentication token.";
                    this.messageClass = "text-danger";
                }
            })
            .catch(error => {
                // This catches network errors or errors thrown from the .then() block
                console.error("Login error:", error);
                this.message = error.message || "Network error or server unreachable. Please try again.";
                this.messageClass = "text-danger";
            });
        }
    }
}
*/




/*
export default{
    template : `
    <div class = "row border">
        <div class = "col" style ="height: 750px;">
            <div class = "border mx-auto mt-5" style ="height: 400px;width : 300px">
                <div>
                    <h2 class="text-center"> Login</h2>
                    <div>
                        <label for="email">Enter your email</label>
                        <input type="text" id="email" v-model="formData.email">
                    </div>
                    <div>
                        <label for="pass">Enter your password</label>
                        <input type="password" id="pass" v-model="formData.password">
                    </div>
                    <div>
                        <button class="btn btn-primary" @click="loginUser"> Login</button>
                    </div>
                    <!-- IMPORTANT: Add this div to display messages -->
                    <div v-if="message" :class="messageClass" class="mt-3">
                        {{ message }}
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
    data:function(){
        return{
            formData:{ // Here formData is a single object that takes both email and password
                email : "",
                password : ""
            },
            message: "",
            messageClass: "" 
        } 
    },
    methods:{
        loginUser: function() {
            fetch('/api/login', {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(this.formData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Login failed");
                }
                return response.json();
            })
            .then(data => {
                console.log("Login response:", data);

                if (data.role === "admin") {
                    this.$router.push('/admin-dashboard');
                } else if (data.role === "user") {
                    this.$router.push('/user-dashboard');
                } else {
                    this.message = "Unknown role. Cannot redirect.";
                    this.messageClass = "text-danger";
                }
            })
            .catch(error => {
                console.error("Login error:", error);
                this.message = "Login failed. Please check your credentials.";
                this.messageClass = "text-danger";
            });
        }

    }
}
*/
