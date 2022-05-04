var updateBtns= document.getElementsByClassName('update-cart')
var removeBtns= document.getElementsByClassName('remove-cart')


console.log('user ', user)


function updateUserOrder(id, action){
    return new Promise(function (resolve){
    var url = '/shop/cart/add-to-cart/'+id+'/'
    
    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
    },
        body: JSON.stringify({'id':id, 'action':action}) //JavaScript object of data to POST
    })
    .then(response => {
        console.log(response.ok)
          return  response.json() //Convert response to JSON
    })
    .then(data => {    
        console.log(data.quantity);
        console.log(data.price);


        var result = data;
        resolve(result);


    }).catch((error) => {
        console.error('Error:', error);
      });

    });
  }

  function removeUserOrder(id, action){
    return new Promise(function (resolve){
    var url = 'remove-from-cart/'+id+'/'
    
    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
    },
        body: JSON.stringify({'id':id, 'action':action}) //JavaScript object of data to POST
    })
    .then(response => {
        console.log(response.ok)
          return  response.json() //Convert response to JSON
    })
    .then(data => {    
        console.log(data.quantity);

        var result = data;
        

        resolve(result);


    }).catch((error) => {
        console.error('Error:', error);
      });

    });
  }


  async function main() {
    

    for (let i =0; i< updateBtns.length; i++){
        updateBtns[i].addEventListener('click',async function(e) {
            e.preventDefault();
            var id = this.dataset.product
            var action =this.dataset.action
            let result = await updateUserOrder(id, action)

            console.log(result);
            console.log(action);

            //quant(result)
            
            
            let quantity=document.getElementsByClassName('quantity');

            quantity[i].innerText=result.quantity
            let total_price=document.getElementsByClassName('total_price');
            total_price[i].innerText=result.price;

            let cart_total=document.getElementById('cart_total');
            cart_total.innerText=result.cart_total;
        })
        
    
    }
    for (let i =0; i< removeBtns.length; i++){
        removeBtns[i].addEventListener('click',async function(e) {
            e.preventDefault();
            var id = this.dataset.product
            var action =this.dataset.action
            let result = await removeUserOrder(id, action)

            console.log(result);
            console.log(action);

            //quant(result)
            let quantity=document.getElementsByClassName('quantity');
            let total_price=document.getElementsByClassName('total_price');
            quantity[i].innerText=result.quantity
            total_price[i].innerText=result.price
            let cart_total=document.getElementById('cart_total');
            cart_total.innerText=result.cart_total;
            console.log(result.cart_total)


        })
    
    }
    
}
main();

