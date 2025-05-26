
var updateBtns=document.getElementsByClassName('update-cart')/*first, query all of the cart items by the class update-cart*/
for (var i=0; i< updateBtns.length; i++ ) {/*then loop through all the buttons*/
    updateBtns[i].addEventListener('click', function(){/*then add event listener onclick...on each iteration, get the queryset which
        is updateBtns and index it with i and it will increment on each iteration...
        then the function will get executed on each click*/
        var productId=this.dataset.product/*then get the product id...product is from the data-product from the onlinestore.html page*/
        var action=this.dataset.action/*get the action...action is from the data-action from the onlinestore.html page...
        in this.dataset.action, the "this" here refers to the clicked item*/
        console.log('productId:', productId, 'action:', action)//then now, just get the two values and console them outd.

        console.log('System_User:', user)/*this user is gotton from main.html, upper side of the page*/
       if (user ==='AnonymousUser'){
           console.log("You are not logged in...please log in")
            addCookieItem(productId, action)
        }else{
           
            updateUserOrder(productId, action)
        }
    })
}


function updateUserOrder(productId, action){
    
    console.log("User is already logged in and is sending data...")
    

    //var url='/ecommerceapp/update_items/'/*send the posted data to this url view template...update-items is from the urls.py...*/
    //var url='/ecommerceapp:update_items/'
   //var url='/update_items/'
    //var url='update_items/'
    var url='update_items'
    //let url = "{% url 'ecommerceapp:update_items' %}"
     
    //to send the posted data, we need to use fetch and the first thing to pass to fetch is the url where we are sending the data to
    //then define the kind of data we are sending to the back-end
    //so the first thing to know the type of data we are sending - here its post data
    fetch(url, {/*this is the fetch API... do some research on FETCH API*/
        method: 'POST',//this is the type of data we are sending - post
        headers: {/**once we are sending post data, we need to pass in some headers with that...the headers are going to be objects */
        'Content-Type': 'application/json',//the C in content and T in type has to be capitals
        
        /**whenever we are sending posting data to the backend in Django, then we need to send a CSRFTOKEN...normally this is
        * done through a form, but since we are not using a form here and we are using Javascripts instead to send the data,you will get an error....
        * to solve this error, we add the csrftoken as below
            */
        'X-CSRFToken':csrftoken,/*this has been copied from the main.html*/
        },

        /**the body is the data we are sending to the backend... this data we want to send as an object...
         * first pass in the product id and action
         * also note that we cant just send this data to the backend as an object, so we need to send it as a string
         */
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    /**once we send the above data, we need to return a promise...the promise is the response we get after we send the data to the view above */
     .then((response) =>{/*this is the promise...we need to first turn the promise value into json data...arrow function*/
     return response.json()/*this ensures that the page reloads when you click the button to add item... not efficient way.
       // he said that he figured out better way and he may add in the premium section...so check out there*/
   })

   .then((data) =>{/**this data here is the promise you got back from the backend...in this case, the data is "item has been added" since from
   the view.py and for 

   def updateItems(request):
        return JsonResponse("item has been added", safe=False) */

       console.log('data:',data)
      location.reload()
   })

    }
    

      
    //this is comments
    
    function addCookieItem(productId, action){
        console.log('Not logged in ...')
    
        if (action=="add"){
            if (cart[productId] == undefined){//we are able to access the cart because its on baseOnlineStore.html file
                cart[productId] ={"quantity" :1}
            }else{
                cart[productId]['quantity']+=1
            }
        }
    
        if (action=="remove"){
           
            cart[productId]['quantity']-=1
            if (cart[productId]['quantity'] <=0){
                console.log('Remove item')
                delete cart[productId];
                }
            }
            console.log('Cart:',cart)
            document.cookie='cart='+ JSON.stringify(cart) + ";domain=;path=/"
            location.reload()
      }


   // })
    //.then((response) =>{/*this is the promise*/
      //  return response.json()/*this ensures that the page reloads when you click the button to add item... not efficient way.
       // he said that he figured out better way and he may add in the premium section...so check out there*/
   // })

   // .then((data) =>{
      //  console.log('data:',data)
     //   location.reload()

//})

//}

/*

var updateBtns=document.getElementsByClassName('update-cart')
for (var i=0; i< updateBtns.length; i++ ) {
    updateBtns[i].addEventListener('click', function(){
        
        var productId=this.dataset.product
        var action=this.dataset.action
        
        console.log('productId:', productId, 'action:', action)
        
        console.log('System_User:', user)

       if (user ==='AnonymousUser'){
           console.log("You are not logged in...please log in")
            
        }else{
           
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log("User is already logged in and is sending data...")
    var url='update_items'
    fetch(url, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken':csrftoken,},
        body:JSON.stringify({'productId': productId, 'action': action})
    })
     .then((response) =>{
     return response.json()  })
   .then((data) =>{
       console.log('data:',data)})}
    */