export default{
    // each row is divided into 12 columns. Here it is divided in the ratio 10:2
    // fs-2 stands for h2 font size
    template : `
    <div class = "row border">
        <div class = "col-10 fs-2 border" >
            Fast Logistics
        </div>
        <div class = "col-2 border" > 
            <router-link class = "btn btn-primary my-2" to="/login"> Login </router-link>
            <router-link class = "btn btn-warning my-2" to="/register"> Register </router-link>
        </div>
    </div>
    `
}