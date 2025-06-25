export default{
    template : `
    <div>    
        <h3 class="my-2"> Welcome {{userData.username}}</h3>
            <div class = "row border">
                <div class = "col-8 border" style ="height: 750px; overflow-y : scroll">
                    <h2> Requested Transactions </h2>
                    <div v-for="t in transactions" class="card mt-2">
                        <table>
                            <thead>

                            </thead>
                            <tbody>
                                
                            </tbody>
                        </table>
                    </div>
                    <h2> Pending Transactions </h2>
                    <div v-for="t in transactions" class="card mt-2">
                        <table>
                            <thead>

                            </thead>
                            <tbody>
                                
                            </tbody>
                        </table>
                    </div>
                    <h2> Paid Transactions </h2>
                    <div v-for="t in transactions" class="card mt-2">
                        <table>
                            <thead>

                            </thead>
                            <tbody>
                                
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class = "col-4 border" style ="height: 750px;">
                    <h2> Create Transactions </h2>    
                    <div class="mb-3">
                        <label for="name" class="form-label"> Transaction name</label>
                        <input type="text" class="form-control" id="name" v-model="transData.name">
                    </div>
                    <div class="mb-3">
                        <label for="type" class="form-label"> Transaction type</label>
                        <input type="text" class="form-control" id="type" v-model="transData.type">
                    </div>
                    <div class="d-flex">
                        <div class="mb-3 mx-2">
                            <label for="source" class="form-label"> Source City</label>
                            <select class="form-select" aria-label="Default select example" v-model="transData.source">
                                <option selected>Open this select menu</option>
                                <option value="Mumbai">Mumbai</option>
                                <option value="Nagpur">Nagpur</option>
                                <option value="Chennai">Chennai</option>
                                <option value="Delhi"> Delhi</option>
                                <option value="Kolkata">Kolkata</option>
                            </select>
                        </div>
                        <div>
                            <label for="destination" class="form-label"> Destination City</label>
                            <select class="form-select" aria-label="Default select example" v-model="transData.destination">
                                <option selected>Open this select menu</option>
                                <option value="Mumbai">Mumbai</option>
                                <option value="Nagpur">Nagpur</option>
                                <option value="Chennai">Chennai</option>
                                <option value="Delhi"> Delhi</option>
                                <option value="Kolkata">Kolkata</option>
                            </select>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="desc" class="form-label">Description</label>
                        <textarea class="form-control" id="desc" rows="3" v-model="transData.desc"></textarea>
                    </div>
                    <div class="mb-3 text-end">
                        <button @click="review" class="btn btn-primary"> Create + </button>
                    </div>
                </div>
            </div>
    </div>` ,
    data : function(){
        return {
            userData : "",
            transactions : null,
            transData : {
                name : '',
                type : '',
                source : '',
                destination :'',
                desc : ''
            }
        }
    },
    mounted(){
        this.loadUser()
        this.loadTrans()
    },
        methods:{
            loadUser(){
                fetch ('/api/home',{
                    method : 'GET',
                    headers : {
                        "Content-Type": "applocation.json",
                        "Authentication-Token": localStorage.getItem("auth-token")
                    }
                })
                .then(response => response.json())
                .then(data => this.userData = data)
            },
            loadTrans(){
                fetch('/api/get',{ // This is to get transaction data
                method : 'GET',
                headers : {
                    "Content-Type": "applocation.json",
                    "Authentication-Token": localStorage.getItem("auth-token")
                    }
                })
                .then(response => response.json())
                .then(data => {
                    this.transactions = data})
            },
            review(){

            }
        }
}   