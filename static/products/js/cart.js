var updateBtns= document.getElementsByClassName('update-cart')
var removeBtns= document.getElementsByClassName('remove-cart')



console.log('user ', user)


function updateUserOrder(slug, action){
    return new Promise(function (resolve){
    var url = 'add-to-cart/'+slug+'/'
    
    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
    },
        body: JSON.stringify({'slug':slug, 'action':action}) //JavaScript object of data to POST
    })
    .then(response => {
        console.log(response.ok)
          return  response.json() //Convert response to JSON
    })
    .then(data => {    
        console.log(data.quantity);

        var result = data.quantity;
        resolve(result);


    }).catch((error) => {
        console.error('Error:', error);
      });

    });
  }

  function removeUserOrder(slug, action){
    return new Promise(function (resolve){
    var url = 'remove-from-cart/'+slug+'/'
    
    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
    },
        body: JSON.stringify({'slug':slug, 'action':action}) //JavaScript object of data to POST
    })
    .then(response => {
        console.log(response.ok)
          return  response.json() //Convert response to JSON
    })
    .then(data => {    
        console.log(data.quantity);

        var result = data.quantity;
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
            var slug = this.dataset.product
            var action =this.dataset.action
            let result = await updateUserOrder(slug, action)

            console.log(result);
            console.log(action);

            //quant(result)
            let quantity=document.getElementsByClassName('quantity');
            
            quantity[i].innerText=result
        })
    
    }
    for (let i =0; i< removeBtns.length; i++){
        removeBtns[i].addEventListener('click',async function(e) {
            e.preventDefault();
            var slug = this.dataset.product
            var action =this.dataset.action
            let result = await removeUserOrder(slug, action)

            console.log(result);
            console.log(action);

            //quant(result)
            let quantity=document.getElementsByClassName('quantity');
            
            quantity[i].innerText=result
        })
    
    }
    
}
main();

