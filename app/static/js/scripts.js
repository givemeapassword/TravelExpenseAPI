$(document).ready(function() {
    // Обработчик отправки формы для расчета стоимости
    $('#trip-form').submit(function(event) {
        event.preventDefault();  // предотвращаем стандартное поведение формы

        // Получаем данные из формы
        const country = $('#country').val();
        const season = $('#season').val();
        const duration = $('#duration').val();
        const num_people = $('#num_people').val();
        const additional_expenses = $('#additional_expenses').val();

        // Отправляем данные на сервер
        $.ajax({
            url: '/api/calculate_trip_cost',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                country: country,
                season: season,
                duration: duration,
                num_people: num_people,
                additional_expenses: additional_expenses
            }),
            success: function(response) {
                // Когда расчет успешен, показываем результаты
                $('#results').removeClass('d-none');  // показываем блок результатов
                $('#total-cost').text(response.total_cost);
                $('#flight-cost').text(response.breakdown.flight);
                $('#accommodation-cost').text(response.breakdown.accommodation);
                $('#food-cost').text(response.breakdown.food);
                $('#transport-cost').text(response.breakdown.transport);
                $('#activities-cost').text(response.breakdown.activities);
                $('#discount').text(response.breakdown.discount);
            },
            error: function(xhr) {
                // Показываем сообщение об ошибке
                alert("Ошибка: " + xhr.responseJSON.error);
            }
        });
    });

    // Обработчик для кнопки "Хотите купить билет?"
    $('#buy-ticket').click(function() {
        // Открываем модальное окно с сообщением о покупке билета
        var myModal = new bootstrap.Modal(document.getElementById('ticketModal'));
        myModal.show();
    });
});
