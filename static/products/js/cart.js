var updateBtns= document.getElementsByClassName('update-cart')
console.log('HHHHHHHHHHHHH')

for (let i =0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var slug =this.dataset.product
        var action =this.dataset.action
        console.log(slug)
        updateUserOrder(slug, action)
    })
}

console.log('user ', user)


function updateUserOrder(slug, action){
    var url = 'add-to-cart/'+slug

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
          return response.json() //Convert response to JSON
    })
    .then(data => {
          commentDiv = document.createElement("div");
          commentDiv.classList.add("comment");
          commentInnerHtml = "<img src="+data.image+" alt='' class='avatar'><div class='comment-card'><small class='author'><i class='far fa-user'></i> "+data.author+"</small><small class='date'><i class='far fa-clock'></i> "+data.date+"</small><div class='comment-content'> "+data.content+"</div><span class='reactions'>25 <i class='fas fa-thumbs-up like'></i>&nbsp;3 <i class='fas fa-thumbs-down dislike'></i></span></div>";
          commentDiv.innerHTML = commentInnerHtml;
          const temp = document.getElementById("temp");
          temp.insertBefore(commentDiv, temp.childNodes[0]);
          form.reset();
    })
  
  }

