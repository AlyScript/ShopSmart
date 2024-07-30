var currentPage = 0;
var itemsPerPage = 10;
var isLoading = false;

function populateSearchProducts() {
    if (isLoading) {
        return;
    }
    isLoading = true;

    var products = window.titles;

    // Calculate the start and end indices for the slice of products to be displayed
    var start = currentPage * itemsPerPage;
    var end = start + itemsPerPage;

    // Only process the products for the current page
    var pageProducts = products.slice(start, end);
    
    fetch('searchHit.html')
        .then(response => response.text())
        .then(data => {
            var container = document.getElementById('product-container');

            let html = '';
            for (var i = 0; i < pageProducts.length; i++) {
                var product = pageProducts[i];

                var card = data
                    .replace('placeholder_image', product.image_link)
                    .replace('placeholderSeller_image', product.source === 'Aldi' ? 'aldi.png' : 'sainsburysLogo2.jpg')                    
                    .replace('placeholder_name', '<a href="#" onclick="loadProductPage(\'' + product.item_title + '\');" class="bold-text">' + product.item_title + '</a>')
                    .replace('quantity', (product.price / product.price_per_kg).toFixed(2) + 'kg')
                    .replace('placeholder_pricePer', '&pound;' + product.price_per_kg + '/kg')
                    .replace('placeholder_price', '<span class="bold-text">' + '&pound;' + product.price + '</span>')
                    .replace('placeholder_link', '<a href="' + (product.source === 'Aldi' ? 'https://groceries.aldi.co.uk' + product.item_link : product.item_link) + '">Original link</a>');

                html += `
                    <div class="col-lg-4 col-md-6 mb-4" style="border: 1px solid rgba(0, 0, 0, 0.1); height: 30%; width: 25%; margin-right: 1px; margin-bottom: 20px;">
                        <div class="card h-100">
                            ${card}
                        </div>
                    </div>
                `;
            }
            container.innerHTML += html;  // Append the new products to the existing ones

            // After all products have been processed, increment the current page and allow more items to be loaded
            currentPage++;
            isLoading = false;
        });
}

var scrollListener = function() {
    // If the user has scrolled within 500 pixels of the bottom, load more items
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 3000) {
        populateSearchProducts();
    }
};

window.addEventListener('scroll', scrollListener);

function clearPage() {
    document.getElementById("header_home_btn").style.opacity = "0.4";
    document.getElementById("header_login_btn").style.opacity = "0.4";
    document.getElementById("header_dod_btn").style.opacity = "0.4";
    document.getElementById("header_set_btn").style.opacity = "0.4";
    
    document.getElementById("placeholder").innerHTML = "";
    document.getElementById("product-container").innerHTML = "";

    currentPage = 0;
    window.removeEventListener('scroll', scrollListener);
}

function startNewSearch() {
    // Add the scroll event listener
    window.addEventListener('scroll', scrollListener);

    // Start the search
    populateSearchProducts();
}

function loadProductPage(productName) {
    // Clear the page
    document.getElementById("product-container").innerHTML = "";

    // Make an AJAX request to the PHP script
    fetch('fetchingdata.php?searchTerm=' + productName)
        .then(response => response.json())
        .then(data => {
            // Check if any products were returned
            if (data.length > 0) {
                // Use the first product for the product page
                var product = data[0];

                // Fetch the product page template
                fetch('productBox.html')
                    .then(response => response.text())
                    .then(template => {
                        // Populate the template with the product data
                        var page = template
                            .replace('placeholder_image1', product.image_link)
                            .replace('placeholder_name1', '<span style="display: block; margin-bottom: 20px;">' + product.item_title + '</span>')
                            .replace('placeholder_pricePer1', '<span style="display: block; margin-bottom: 20px;">Price per Quantity: &pound;' + product.price_per_kg + '/kg</span>')
                            .replace('placeholder_price1', '<span style="display: block; margin-bottom: 20px;">Price: &pound;' + product.price + '</span>')
                            .replace('placeholder_button', '<button class="basket-button" style="background-color: black; color: white; border-radius: 0; width: 10%; transition: background-color 0.5s;" onmouseover="this.style.backgroundColor=\'grey\'" onmouseout="this.style.backgroundColor=\'black\'" onclick="addToBasket(\'' + encodeURIComponent(product.image_link) + '\', \'' + product.item_title + '\', \'' + product.price + '\', \'' + product.price_per_kg + '\', \'' + product.source + '\', \'' + (product.source === 'Aldi' ? 'https://groceries.aldi.co.uk' + product.item_link : product.item_link) + '\')">Add to Basket</button>')
                            .replace('placeholder_link', '<a href="' + (product.source === 'Aldi' ? 'https://groceries.aldi.co.uk' + product.item_link : product.item_link) + '">Original link</a>');
                        document.getElementById('product-container').innerHTML = page;
                    });
            }
        });
}

var productBasket = JSON.parse(localStorage.getItem('productBasket')) || [];

window.addToBasket = function(image, name, pricePer, price, source, url) {
    image = decodeURIComponent(image);
    var product = {
        image: image,
        name: name,
        pricePer: pricePer,
        price: price,
        source: source,
        url: url,
        quantity: 1  // Add a quantity attribute
    };

    // Check if a product with the same name and image URL already exists in the productBasket
    var existingProductIndex = productBasket.findIndex(function(p) {
        return p.name === product.name && p.image === product.image;
    });

    if (existingProductIndex !== -1) {
        // If the product already exists, increase its quantity
        productBasket[existingProductIndex].quantity += 1;
    } else {
        // If the product doesn't exist, add it to the productBasket
        productBasket.push(product);
    }

    // Save the updated productBasket back to localStorage
    localStorage.setItem('productBasket', JSON.stringify(productBasket));
}
