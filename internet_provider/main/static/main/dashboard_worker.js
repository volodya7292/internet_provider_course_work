customer_info = document.getElementById("customer_info");

function onCustomerChange(e) {
    customer_info.style.visibility = "visible";

    $.ajax({
        type: 'GET',
        url: "get_customer",
        data: { "id": e.value },
        success: function (response) {
            $("#customer_name").text(response.name);
            $("#customer_address").text(response.address);
            $("#customer_phone").text(response.phone);
            $("#customer_email").text(response.email);
            $("#customer_balance").text(response.balance);
        },
        error: function (response) {
            console.log(response)
        }
    });
}