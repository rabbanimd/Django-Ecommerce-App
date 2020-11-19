

function updateUserOrder(itemId,action) {
    console.log('user is logged in ....')
    var url='/update_item/'
    fetch(url,
        {
            method:'POST',
            headers:{
                'content-Type':'application/Json'
            },
        })
}
  $('.cart').click(function () {
                    console.log('clicked');
            });