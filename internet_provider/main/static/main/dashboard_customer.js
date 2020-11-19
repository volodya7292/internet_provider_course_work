function onCustomerServiceChange() {
    $("#service_id").val(document.getElementById("customer_services").value);
    
    $.ajax({
        type: "GET",
        url: "get_service",
        data: { "service_id": document.getElementById("customer_services").value },
        success: function (response) {
            const obj = JSON.parse(response)[0]
            $("#customer_service_static_ip").text(obj.fields.static_ip ? "Yes" : "No");
            $("#customer_service_traffic").text(Math.floor(obj.fields.traffic / 1e6) + " МБ");
            $("#customer_tariff_name").text(obj.fields.tariff.name);
            $("#customer_tariff_price").text(obj.fields.tariff.price + " UAH");
            $("#customer_tariff_speed").text(obj.fields.tariff.speed + " MBit/s");
            $("#customer_tariff_desc").text(obj.fields.tariff.description);

            const limit = obj.fields.tariff.limit;
            $("#customer_tariff_limit").text(limit >= 9999999 ? "Unlimited" : (limit + " МB"));
        },
        error: function (response) {
            console.log(response)
        }
    });
}

onCustomerServiceChange()