export default{
    template : `
    <div class = "row border">
        <div class = "col" style ="height: 750px;">
            <div class = "border mx-auto mt-5" style ="height: 400px;width : 300px">
                <div>
                    <h2 class="text-center"> Register</h2> <!-- Changed from Login to Register -->
                    <div>
                        <label for="email">Enter your email</label>
                        <input type="text" id="email" v-model="formData.email" class="form-control">
                    </div>
                    <div class="mt-3">
                        <label for="username">Enter your username</label>
                        <input type="text" id="username" v-model="formData.username" class="form-control"> <!-- Changed type to text -->
                    </div>
                    <div class="mt-3">
                        <label for="pass">Enter your password</label>
                        <input type="password" id="pass" v-model="formData.password" class="form-control">
                    </div>
                    <div class="mt-4">
                        <button class="btn btn-primary" @click="addUser"> Register</button> <!-- Changed button text and method to addUser -->
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
            formData:{ // Here formData is a single object that takes both email, password, and username
                email : "",
                password : "",
                username : "" // Correctly initialized
            },
            message: "", // For displaying messages from the server
            messageClass: "" // For styling messages (e.g., text-success, text-danger)
        } 
    },
    methods:{
        addUser: function() { // Renamed from loginUser to addUser
            this.message = ""; // Clear previous messages
            this.messageClass = "";

            // IMPORTANT: Updated client-side validation to include username
            if (!this.formData.email || !this.formData.username || !this.formData.password) {
                this.message = "Email, username, and password are required!";
                this.messageClass = "text-danger";
                return;
            }

            console.log("Sending registration data:", this.formData); // Debugging: See what's being sent

            fetch('/api/register', { // Correct API endpoint
                method: "POST",
                headers: { 
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(this.formData)
            })
            .then(response => {
                if (response.ok) {
                    return response.json(); 
                } else {
                    return response.json().then(errorData => {
                        throw new Error(errorData.message || 'Registration failed on server.'); // Updated error message
                    });
                }
            })
            .then(data => {
                console.log("Registration response:", data); // Updated console log message
                
                // IMPORTANT: Removed all login-specific logic (localStorage, auth-token, role-based redirect)
                this.message = data.messsage || "Registration successful!"; // Backend sends 'messsage' for success
                this.messageClass = "text-success";

                // Redirect to login page after successful registration
                this.$router.push('/login'); 
            })
            .catch(error => {
                console.error("Registration error:", error); // Updated console log message
                this.message = error.message || "Network error or server unreachable. Please try again."; // Updated message
                this.messageClass = "text-danger";
            });
        }
    }
}
