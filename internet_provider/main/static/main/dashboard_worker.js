let customers = [];
let customer_services = [];

$.ajax({
    type: 'GET',
    url: "get_customers",
    data: {},
    success: function (response) {
        customers = JSON.parse(response);
        $("#customers").empty();

        for (let i = 0; i < customers.length; i++) {
            const customer = customers[i];
            var option = $('<option></option>').attr("value", i).text(customer.fields.name);

            $.ajax({
                type: 'GET',
                url: "get_customer_services",
                data: { "customer_id": customer.pk },
                success: function (response) {
                    customer_services = JSON.parse(response);

                    $("#customers_table").append(`<tr>
                        <td>${customer.fields.name}</td>
                        <td>${customer.fields.phone}</td>
                        <td>${customer.fields.balance} UAH</td>
                        <td>${customer.fields.address}</td>
                        <td>${customer_services[0].fields.tariff.name}</td>
                        <td>${customer.fields.user[0]}</td>
                    </tr>`);
                },
                error: function (response) {
                    console.log(response)
                }
            });

            $("#customers").append(option);

            console.log(customer);
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

    $("#customer_info_panel").css("visibility", "visible");
    $("#customer_info").css("visibility", "visible");

    $("#customer_name").text(obj.fields.name);
    $("#customer_address").text(obj.fields.address);
    $("#customer_phone").text(obj.fields.phone);
    $("#customer_username").text(obj.fields.user[0]);
    $("#customer_balance").text(obj.fields.balance + " ГРН");

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
    $("#customer_service_static_ip").text(obj.fields.static_ip ? "Так" : "Нi");
    $("#customer_service_traffic").text(Math.floor(obj.fields.traffic / 1e6) + " МБ");
    $("#customer_tariff_name").text(obj.fields.tariff.name);
    $("#customer_tariff_price").text(obj.fields.tariff.price + " ГРН");
    $("#customer_tariff_speed").text(obj.fields.tariff.speed + " Мбiт/с");
    $("#customer_tariff_desc").text(obj.fields.tariff.description);

    const limit = obj.fields.tariff.limit;
    $("#customer_tariff_limit").text(limit >= 9999999 ? "Безлiмiт" : (limit + " МБ"));
}


