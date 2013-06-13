function ListController($scope, $routeParams, $http, $cookieStore, $cookies) {
 var headers = {};
 headers['Cookie'] = $scope.sessionCookie;
 currentListId = $routeParams.listId;
 $http({method: 'GET', url: serverUrl+'/api/v1/Lists/'+currentListId, headers: headers}).
    success(function(data, status, headers, config) {
        $scope.items = data;
        if (localStorage && localStorage[currentListId]) {
            var jsonItems = localStorage[currentListId];
            $scope.items = JSON.parse(jsonItems);
        }
        var listItems = document.getElementById('sortable').getElementsByTagName('li');
        for (var i = 0; i < listItems.length; ++i) {
            Hammer(listItems[i], {
                swipe_velocity : 0.2
            }).on("swiperight", swipeRight);
        }
    }).
    error(function(data, status, headers, config) {
  });

    addItem = function(description, id, quantity) {
        var found = false;
        for (var item in $scope.items)
        {
            if ($scope.items[item].description === description) {
                $scope.items[item].quantity = parseInt(quantity, 10);
                if (!$scope.items[item].id)
                {
                    $scope.items[item].id = id;
                }
                found  = true;
                break;
            }
        }
        if (!found) {
            $scope.items.push({description: description, id: id, quantity: quantity});
        }
        console.log(JSON.stringify($scope.items));
    };

    $scope.itemsJSON = JSON.stringify($scope.itmes);

    window.setInterval(function(){
        newItemsJSON = JSON.stringify($scope.items);
        if (newItemsJSON != $scope.itemsJSON) {
            if (localStorage)
            {
                localStorage[currentListId] = newItemsJSON;
                $scope.itemsJSON = newItemsJSON;
            }
        }
    },1000);

    $scope.sortableOptions = {
        tolerance: 'pointer',
        handle: '.icon-align-justify',
            axis: 'y',
            delay: 100,
            distance: 10
    };

    var modalShown = false;
    var results = {};
    $('#modal-list-item').on('shown', function () {
        modalShown = true;
        $('#product-query').focus();
    });
    $('#modal-list-item').on('hidden', function () {
        modalShown = false;
        $('#product-query').val('');
    });
    $('#modal-form').on('submit', function(e) {
        var name = $('#product-query').val();
        var quantity = $('#quantity').val();
        $.ajax({
            url: '/api/v1/Lists/'+currentListId,
            type: 'POST',
            data: {'description': name, 'quantity': quantity, 'key': results[name]},
            success: function(data) {
                console.log(data);
                $scope.$apply(function () {
                    addItem(data.description, data.id, data.quantity);
                });
            }
        });
        return false;
    });
    $('#modal-form-submit').on('click', function(e){
        e.preventDefault();
        $('#modal-form').submit();
        $('#modal-list-item').modal('hide');
    });

    $("#product-query").typeahead({
        minLength: 3,
        items: 20,
        source: function(query, process) {
            results = {};
            $.get('/Products', { q: query.toLowerCase() }, function(data) {
                var newData = [];
                $.each(data, function(){
                    newData.push(this.name);
                    results[this.name] = this.id;
                });
                process(newData);
            });
        },
        matcher: function(item) {
            return true;
        },
        highlighter: function (item) {
            var terms = this.query.split(' ');
            var regexp_string = '';
            var replace_string = "<strong>";
            for (var i = 0; i < terms.length; ++i) {
                if (i !== 0)
                {
                    regexp_string += '|';
                }
                regexp_string += '(' + terms[i] + ')';
                replace_string += "$" + (i+1);
            }
            replace_string += "</strong>";
            var regex = new RegExp( regexp_string, 'gi' );
            item = item.replace( regex, replace_string );
            return item;
        }
    });

    $(document).keypress(function(e){
        e = window.event || e;
        if (String.fromCharCode(e.charCode) == 'a') {
            $('#modal-list-item').modal();
        }
        if (e.charCode == 13) {
            if (modalShown) {
                $('#modal-form').submit();
                $('#modal-list-item').modal('hide');
            }
        }
    });

} // ListController


function transform(deleteBtn, style) {
    deleteBtn.style.transform = style;
    deleteBtn.style.webkitTransform = style;
    deleteBtn.style.mozTransform = style;
    deleteBtn.style.oTransform = style;
}

// List handling
function deleteItem(e) {
    var currentDiv = e.target.parentNode;
    var name = currentDiv.id;
    var list_id = currentListId
    $.ajax({
        url: '/api/v1/Lists/'+list_id+'/'+name,
        type: 'DELETE',
        success: function() {
            currentDiv.parentNode.parentNode.removeChild(currentDiv.parentNode);
        }
    });
}

function showDeleteButton(currentDiv)
{
    var deleteBtn = document.createElement("button");
    deleteBtn.appendChild(document.createTextNode("delete"));
    deleteBtn.className += ("delete-btn btn btn-danger btn-small");
    deleteBtn.style = "btn";
    deleteBtn.style.position = "absolute";
    deleteBtn.style.right = "6px";
    currentDiv.appendChild(deleteBtn);
    deleteBtn.style.top = (currentDiv.clientHeight - deleteBtn.clientHeight) / 2 + "px";
    deleteBtn.style.opacity = 1;
    deleteBtn.onclick = deleteItem;
}

function hideDeleteButton(currentDiv)
{
    var deleteBtn = $(currentDiv).children(".delete-btn")[0];
    //deleteBtn.style.opacity = 0;
    //transform(deleteBtn, "translate3d(20px,0,0)"); // use 3d for hardware acceleration
    currentDiv.removeChild(deleteBtn);
}

function swipeRight(e) {
    var currentDiv = e.target;
    if (currentDiv.localName != "div") {
        currentDiv = e.target.firstChild;
    }
    var button = $(".delete-btn");
    if (button.length === 0) {
        showDeleteButton(currentDiv);
        button.on("click", function () { alert('deleted internally'); });
    } else {
        var buttonDiv = button[0].parentNode;
        hideDeleteButton(buttonDiv);
        if (buttonDiv != currentDiv) {
            showDeleteButton(currentDiv);
        }
    }
}


