export default {
    template: `
    <div class="container mt-4">
        <h2 class="text-center mb-4">Admin Dashboard</h2>
        <div v-if="loading" class="text-center">Loading admin data...</div>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        
        <div v-if="!loading && !error">
            <h3 class="mb-3">All Users</h3>
            <table class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Email</th>
                        <th>Username</th>
                        <th>Active</th>
                        <th>Roles</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in users" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.active ? 'Yes' : 'No' }}</td>
                        <td>{{ user.roles.join(', ') }}</td>
                    </tr>
                    <tr v-if="users.length === 0">
                        <td colspan="5" class="text-center">No users found.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    `,
    data() {
        return {
            users: [],
            loading: true,
            error: null,
        };
    },
    // The created lifecycle hook is called after the instance is created
    // but before it's mounted to the DOM. This is a good place to fetch data.
    created() {
        this.fetchAdminData();
    },
    methods: {
        fetchAdminData() {
            this.loading = true;
            this.error = null;
            const authToken = localStorage.getItem('auth-token');

            if (!authToken) {
                this.error = "Authentication token not found. Please log in.";
                this.loading = false;
                this.$router.push('/login'); // Redirect to login if no token
                return;
            }

            fetch('/api/admin', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': authToken // Send the token
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    // Handle non-200 responses (e.g., 401 Unauthorized, 403 Forbidden)
                    return response.json().then(errData => {
                        throw new Error(errData.message || 'Failed to fetch admin data.');
                    });
                }
            })
            .then(data => {
                console.log("Admin Data:", data);
                this.users = data.users || []; // Assuming backend sends 'users' array
                this.loading = false;
            })
            .catch(error => {
                console.error("Error fetching admin data:", error);
                this.error = error.message || "An error occurred while fetching data.";
                this.loading = false;
            });
        }
    }
};
