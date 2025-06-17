export default{
    template : `
    <div class = "row border">
        <div class = "col" style ="height: 750px;">
            <div class = "border mx-auto mt-5" style ="height: 400px;width : 300px">
                {{userData.email}}
                {{userData.username}}
                {{userData.password}}
            </div>
        </div>
    </div>` ,
    data : function(){
        return {
            userData : ""
        }
    },
    mounted(){
        fetch('/api/home',{
            method : 'GET',
            headers : {
                "Content-Type": "applocation.json",
                "Authentication-Token": localStorage.getItem("auth-token")
                }
            })
            .then(response => response.json())
            .then(data => this.userData = data)
        }
}