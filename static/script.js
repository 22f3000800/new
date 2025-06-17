// Access createApp from the globally available 'Vue' object
const { createApp } = Vue;

// Access createRouter and createWebHistory from the globally available 'VueRouter' object
const { createRouter, createWebHistory } = VueRouter;

// Import your components (paths relative to this script.js file remain the same)
import Home from "./components/Home.js";
import Login from "./components/Login.js";
import Register from "./components/Register.js";
import Navbar from "./components/Navbar.js";
import Footer from "./components/Footer.js";
import Dashboard from "./components/Dashboard.js";
import AdminDashboard from "./components/Admin_Dashboard.js"

// 1. Define your routes for Vue Router 4
const routes = [
    { path: '/', component: Home },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/user-dashboard', component: Dashboard},
    { path: '/admin-dashboard', component: AdminDashboard, meta: { requiresAuth: true, roles: ['admin'] }}
];

// 2. Create the router instance for Vue Router 4
const router = createRouter({
    history: createWebHistory(), // Uses HTML5 History API for clean URLs (e.g., /login)
    routes // Shorthand for `routes: routes`
});

// 3. Create your Vue 3 application instance
const app = createApp({
    // Main template for the root component.
    // Includes <nav-bar> and <foot> as global components,
    // and <router-view> for rendering components based on the current route.
    // in template , class = "container" , center aligns everything
    template: `
    <div class ="container"> 
        <nav-bar></nav-bar>
        <router-view></router-view>
        <foot></foot>
    </div>
    `,
    // Data properties for the root component (if needed)
    data() {
        return {
            // This 'section' data is accessible within this root app's template
            section : "Frontend"
        };
    },
    // Register global components that are used directly in the root template
    components: {
        "nav-bar": Navbar, // Maps the custom element <nav-bar> to the imported Navbar component
        "foot": Footer,    // Maps the custom element <foot> to the imported Footer component
    }
});

// 4. Register the router with your Vue 3 application
// This makes router functionalities (like <router-link> and <router-view>) available throughout your app.
app.use(router);

// 5. Mount the Vue application to the HTML element with id="app"
app.mount("#app");