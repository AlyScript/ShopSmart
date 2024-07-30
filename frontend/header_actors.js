function updateTotalPrice() {
    var productBasket = JSON.parse(localStorage.getItem('productBasket')) || [];
    var totalPrice = 0;

    productBasket.forEach(function(product) {
        totalPrice += parseFloat(product.price) * parseFloat(product.quantity);
    });

    console.log('Total price:', totalPrice);  // Add this line

    document.getElementById('totalPrice').textContent = '\u00A3' + totalPrice.toFixed(2);
}

window.click_page = async function(page) {

    document.getElementById("header_home_btn").style.opacity = "0.4";
    document.getElementById("header_login_btn").style.opacity = "0.4";
    document.getElementById("header_dod_btn").style.opacity = "0.4";
    document.getElementById("header_set_btn").style.opacity = "0.4";

    document.getElementById("placeholder").innerHTML = "";
    document.getElementById("product-container").innerHTML = "";


    if (page == "bask") {
        document.getElementById("header_dod_btn").style.opacity = "1.0";
        try {
            let response = await fetch("basket.html");
            let data = await response.text();
            document.getElementById("placeholder").innerHTML = data;
    
                // Populate the basket after the basket.html content has been inserted
                var productBasket = JSON.parse(localStorage.getItem('productBasket')) || [];
                var itemsContainer = document.getElementById('items');

                // Create table
                var table = document.createElement('table');
                table.style.width = '100%';
                table.style.tableLayout = 'fixed';
                table.style.borderSpacing = '1000px';

                // Create table header
                var thead = document.createElement('thead');
                var headerRow = document.createElement('tr');

                var headers = ['Image', 'Name', 'Source', 'Quantity', 'Price', 'Total'];
                headers.forEach(function(header) {
                    var th = document.createElement('th');
                    th.textContent = header;
                    headerRow.appendChild(th);
                });

                thead.appendChild(headerRow);
                table.appendChild(thead);

                // Create table body
                var tbody = document.createElement('tbody');
                productBasket.forEach(function(product, index) {
                    var row = document.createElement('tr');

                    var imageCell = document.createElement('td');
                    var img = document.createElement('img');
                    img.src = product.image;
                    img.alt = product.name;
                    img.width = '120';
                    img.height = '150';
                    imageCell.appendChild(img);

                    var nameCell = document.createElement('td');

                    var nameLink = document.createElement('a');
                    nameLink.href = product.url;  // Replace with the actual URL
                    nameLink.target = '_blank';  // Open the URL in a new tab
                    nameLink.textContent = product.name;
                    nameLink.className = 'bold-text';
                    nameCell.appendChild(nameLink);

                    var sourceCell = document.createElement('td');
                    sourceCell.textContent = product.source;

                    var quantityCell = document.createElement('td');
                    quantityCell.textContent = product.quantity;  // Assuming each product has a 'quantity' property

                    var priceCell = document.createElement('td');
                    priceCell.textContent = '\u00A3' + product.price;

                    var quantityChangeCell = document.createElement('td');

                    var totalCell = document.createElement('td');
                    totalCell.textContent = '\u00A3' + (product.price * product.quantity).toFixed(2);

                    var increaseButton = document.createElement('button');
                    increaseButton.textContent = '+';
                    increaseButton.addEventListener('click', function() {
                        product.quantity++;
                        quantityCell.textContent = product.quantity;
                        totalCell.textContent = '\u00A3' + (product.price * product.quantity).toFixed(2);
                        localStorage.setItem('productBasket', JSON.stringify(productBasket));
                        updateTotalPrice();
                    });

                    var decreaseButton = document.createElement('button');
                    decreaseButton.textContent = '-';
                    decreaseButton.addEventListener('click', function() {
                        if (product.quantity > 0) {
                            product.quantity--;
                            quantityCell.textContent = product.quantity;
                            totalCell.textContent = '\u00A3' + (product.price * product.quantity).toFixed(2);
                            localStorage.setItem('productBasket', JSON.stringify(productBasket));
                            updateTotalPrice();
                        }
                    });

                    var deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.addEventListener('click', function() {
                        // Remove product from productBasket
                        var index = productBasket.indexOf(product);
                        if (index > -1) {
                            productBasket.splice(index, 1);}
                        localStorage.setItem('productBasket', JSON.stringify(productBasket));
                        if (row.parentNode) {
                            row.parentNode.removeChild(row);
                        }
                        updateTotalPrice();
                        }
                    );

                    deleteButton.addEventListener('click', function() {
                        // Remove product from productBasket
                        var index = productBasket.indexOf(product);
                        if (index > -1) {
                            productBasket.splice(index, 1);
                        }
                    
                        // Decrease count based on product's source
                        if (product.source === 'Sainsburys') {
                            sainsburys_count_text -= product.quantity;
                        } else if (product.source === 'Aldi') {
                            aldi_count_text -= product.quantity;
                        }
                    
                        document.getElementById('sainsburys_count_text').textContent = sainsburys_count_text + ' items';
                        document.getElementById('aldi_count_text').textContent = aldi_count_text + ' items';
                        localStorage.setItem('productBasket', JSON.stringify(productBasket));
                        if (row.parentNode) {
                            row.parentNode.removeChild(row);
                        }
                    });

                    increaseButton.style.width = '50px';
                    decreaseButton.style.width = '50px';
                    deleteButton.style.width = '120px';                    
                    increaseButton.style.marginRight = '10px';
                    decreaseButton.style.marginLeft = '10px';
                    deleteButton.style.marginTop = '10px';
                    increaseButton.style.backgroundColor = 'black';
                    decreaseButton.style.backgroundColor = 'black';
                    deleteButton.style.backgroundColor = 'black';
                    increaseButton.style.color = 'white';
                    decreaseButton.style.color = 'white';
                    deleteButton.style.color = 'white';

                    row.appendChild(imageCell);
                    row.appendChild(nameCell);
                    row.appendChild(sourceCell);
                    row.appendChild(quantityCell);
                    row.appendChild(priceCell);
                    row.appendChild(totalCell);
                    quantityChangeCell.appendChild(increaseButton);
                    quantityChangeCell.appendChild(decreaseButton);
                    quantityChangeCell.appendChild(deleteButton);
                    row.appendChild(quantityChangeCell);

                    tbody.appendChild(row);

                });
                // Initialize counts
                var sainsburys_count_text = 0;
                var aldi_count_text = 0;

                productBasket.forEach(function(product) {
                    // Update counts based on source
                    if (product.source === 'Sainsburys') {
                        sainsburys_count_text += product.quantity;
                    } else if (product.source === 'Aldi') {
                        aldi_count_text += product.quantity;
                    }
                });
                document.getElementById('sainsburys_count_text').textContent = sainsburys_count_text + ' items';
                document.getElementById('aldi_count_text').textContent = aldi_count_text + ' items';
                updateTotalPrice();

                table.appendChild(tbody);

                // Append table to itemsContainer
                itemsContainer.appendChild(table);
            } catch (error) {
                console.log(error);
            }
    }else if (page == "home") {
        document.getElementById("header_home_btn").style.opacity = "1.0";
        try {
            let response = await fetch("new_homepage.html");
            let data = await response.text();
            document.getElementById("placeholder").innerHTML = data;
            populateProducts();
        } catch (error) {
            console.log(error);
        }
    } else if (page == "login") {
        document.getElementById("header_login_btn").style.opacity = "1.0";
        try {
            let response = await fetch("login_page.html");
            let data = await response.text();
            document.getElementById("placeholder").innerHTML = data;
            populateProducts();
        } catch (error) {
            console.log(error);
        }
    } else if (page == "set") {
        document.getElementById("header_set_btn").style.opacity = "1.0";
        try {
            let response = await fetch("accountsettings.html");
            let data = await response.text();
            document.getElementById("placeholder").innerHTML = data;
        } catch (error) {
            console.log(error);
        }
}

function populateProducts() {
    var products = [
        { name: 'Product 1', category: 'Fruit', quantity: '100g', price: '$99.99', 
        pricePer: '60p/100g', image1: 'placeholder1.png', image2: 'placeholder1.png'},
        { name: 'Product 2', category: 'Fruit', quantity: '103g', price: '$89.99', 
        pricePer: '60p/100g', image1: 'placeholder1.png', image2: 'placeholder1.png'},
        { name: 'Product 3', category: 'Fruit', quantity: '106g', price: '$79.99', 
        pricePer: '60p/100g', image1: 'placeholder1.png', image2: 'placeholder1.png'},
        { name: 'Product 4', category: 'Fruit', quantity: '102g', price: '$89.99', 
        pricePer: '60p/100g', image1: 'placeholder1.png', image2: 'placeholder1.png'},
    ];

    fetch('searchHit.html')
        .then(response => response.text())
        .then(data => {
            var container = document.getElementById('product-container');

            for (var i = 0; i < products.length; i++) {
                var product = products[i];

                var card = data
                    .replace('placeholder_image', product.image1)
                    .replace('placeholderSeller_image', product.image2)
                    .replace('placeholder_name', '<span class="bold-text">' + product.name + '</span>')
                    .replace('placeholder_category', product.category)
                    .replace('quantity', product.quantity)
                    .replace('placeholder_pricePer', product.pricePer)
                    .replace('placeholder_price', '<span class="bold-text">' + product.price + '</span>');

                container.innerHTML += `
                    <div class="col-lg-4 col-md-6 mb-4">
                        <div class="card h-100">
                            ${card}
                        </div>
                    </div>
                `;
            }
        });
}}