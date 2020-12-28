var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i< updateBtns.length; i++){
		updateBtns[i].addEventListener('click', function(){
		var productId= this.dataset.product
		var action = this.dataset.action
		console.log('productd:', productId, 'action:', action)
		
		console.log('user:', user)
		if(user === 'AnonymousUser'){
			console.log('Not logged in')
			} else{
                updateUserOrder(productId, action)
            }
		})
	}

function updateUserOrder(productId, action){
	console.log('user logged in, sending data...')

	var url = '/update_item/'

	fetch(url, {
	    method: 'POST',
	    headers:{
	        'Content-Type': 'appliction/json',
	        'X-CSRFToken': csrftoken,      //add csrf token from documentation
	    },
	    body: JSON.stringify({'productId': productId, 'action': action})
	})
	.then((response) => {
	    return response.json()
	})
	.then((data) => {
        console.log('data:', data)
        location.reload()
	})
}
	