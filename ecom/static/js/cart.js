var updateBtns = document.getElementsByClassName('update-cart')

for(i=0; i<updateBtns.length;i++)
{
    updateBtns[i].addEventListener('click',function(){
        var productid = this.dataset.product
        var action = this.dataset.action
        console.log('productId: ',productid,'Action: ',action)

        console.log('User: ',user)
        if(user == 'AnonymousUser')
        {
            console.log('Not logged in')
        }
        else
        {
            updateUserOrder(productid,action)
        }
    })
}

function updateUserOrder(productId,action)
{
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data)=>{
        console.log('Data: ',data)
        location.reload()
    });
}