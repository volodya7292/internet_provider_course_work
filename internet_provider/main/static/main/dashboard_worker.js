let customers = [];
let customer_services = [];

$.ajax({
    type: 'get',
    url: "get_customers",
    data: {},
    success: function (response) {
        customers = JSON.parse(response);
        $("#customers").empty();

        for (let i = 0; i < customers.length; i++) {
            const customer = customers[i];
            var option = $('<option></option>').attr("value", i).text(customer.fields.name);
            $("#customers").append(option);
        }

        if (customers.length > 0) {
            onCustomerChange();
        }
    },
    error: function (response) {
        console.log(response)
    }
});

function onCustomerChange() {
    const obj = customers[document.getElementById("customers").value];

    $("#customer_info").css("visibility", "visible");

    $("#customer_name").text(obj.fields.name);
    $("#customer_address").text(obj.fields.address);
    $("#customer_phone").text(obj.fields.phone);
    $("#customer_email").text(obj.fields.email);
    $("#customer_balance").text(obj.fields.balance);

    $("#customer_services_info").css("visibility", "collapse");

    $.ajax({
        type: 'GET',
        url: "get_customer_services",
        data: { "customer_id": obj.pk },
        success: function (response) {
            customer_services = JSON.parse(response);
            $("#customer_services").empty();

            for (let i = 0; i < customer_services.length; i++) {
                const service = customer_services[i];
                var option = $('<option></option>').attr("value", i).text(service.fields.address);
                $("#customer_services").append(option);
            }

            if (customer_services.length > 0) {
                onCustomerServiceChange(customer_services[0]);
                $("#customer_services_info").css("visibility", "visible");
            }
        },
        error: function (response) {
            console.log(response)
        }
    });
}

function onCustomerServiceChange() {
    const obj = customer_services[document.getElementById("customer_services").value];
    $("#customer_service_static_ip").text(obj.fields.static_ip ? "Yes" : "No");
}


