//   Когда `html`  документ  загружен
$(document).ready(function () {

    // Перехватываем отправку формы
    $('#Massage').submit(function () {
        // Получаем данные из формы, и создаем объекта
        const dataVar = {
            get_user_name: $(this)[0][0].value,
            text_message: $(this)[0][1].value,
        };
        // Отладочная информация
        console.log(dataVar)

        // Отправляем `ajax` запрос
        $.ajax({
            // Тело сообщения
            method: "POST", // Http Метод отправки данных на сервер
            url: $(this).attr("action"), // Берем url из ранее созданной переменной в шаблоне
            data: dataVar, // Данные на сервер

            // Вызовется если при отправке возникли ошибки
            error: function (response) {
                const exceptionVar = "Ошибка отправки" + JSON.stringify(response)
                alert(exceptionVar);
                console.log(exceptionVar)
            }
        }).done(function (msg) { // Получаем ответ от сервера, и обрабатываем его.
            alert(JSON.stringify(msg))
            console.log(msg)
        });

        // Остановить перезагрузку страницы
        return false;
    });


    function UpdateWidget() {

    }
})