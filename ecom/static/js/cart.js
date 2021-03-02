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
            console.log('User is logged in.')
        }
    })
}
