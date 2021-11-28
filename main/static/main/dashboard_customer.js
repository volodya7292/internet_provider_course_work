function onCustomerServiceChange() {
    $("#service_id").val(document.getElementById("customer_services").value);
    $("#service_id2").val(document.getElementById("customer_services").value);

    $.ajax({
        type: "GET",
        url: "get_service",
        data: { "service_id": document.getElementById("customer_services").value },
        success: function (response) {
            const obj = JSON.parse(response)[0];
            $("#customer_service_static_ip").text(obj.fields.static_ip ? "Так" : "Нi");
            $("#customer_service_traffic").text(Math.floor(obj.fields.traffic / 1e6) + " МБ");
            $("#customer_tariff_name").text(obj.fields.tariff.name);
            $("#customer_tariff_price").text(obj.fields.tariff.price + " ГРН");
            $("#customer_tariff_speed").text(obj.fields.tariff.speed + " Мбiт/с");
            $("#customer_tariff_desc").text(obj.fields.tariff.description);

            const limit = obj.fields.tariff.limit;
            $("#customer_tariff_limit").text(limit >= 9999999 ? "Безлiмiт" : (limit + " МБ"));

            console.log(obj);
            $("#pay_for_tariff").css("display", (+obj.fields.customer.balance >= +obj.fields.tariff.price) ? "block" : "none");
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function payForTariff() {
    document.location.reload();
}

onCustomerServiceChange()

$.ajax({
    type: "GET",
    url: "get_payment_history",
    data: {},
    success: function (response) {
        const obj = JSON.parse(response);

        for (let i = 0; i < obj.length; i++) {
            let payment = obj[i];

            let date = new Date(payment.fields.time);
            let date_f = date.toLocaleString();

            $("#payments_table").append(`<tr>
                <td>${date_f}</td>
                <td>${payment.fields.income_expense} ГРН</td>
                <td>${payment.fields.balance} ГРН</td>
                <td>${payment.fields.comment}</td>
            </tr>`);
        }
    },
    error: function (response) {
        console.log(response);
    }
});