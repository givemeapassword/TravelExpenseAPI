$(document).ready(function() {
    // Обработчик отправки формы
    $('#trip-form').on('submit', function(e) {
        e.preventDefault();

        const country = $('#country').val();
        const season = $('#season').val();
        const duration = $('#duration').val();
        const num_people = $('#num_people').val();
        const additional_expenses = $('#additional_expenses').val();

        // Отправка данных на сервер для расчета стоимости
        $.ajax({
            url: '/api/calculate_trip_cost',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                country: country,
                season: season,
                duration: duration,
                num_people: num_people,
                additional_expenses: additional_expenses
            }),
            success: function(response) {
                // Отображаем результаты на странице
                $('#results').removeClass('d-none');
                $('#total-cost').text(response.total_cost);
                $('#flight-cost').text(response.breakdown.flight);
                $('#accommodation-cost').text(response.breakdown.accommodation);
                $('#food-cost').text(response.breakdown.food);
                $('#transport-cost').text(response.breakdown.transport);
                $('#activities-cost').text(response.breakdown.activities);
                $('#discount').text(response.breakdown.discount);
            },
            error: function(error) {
                alert('Произошла ошибка при расчете стоимости!');
            }
        });

        // Дополнительно можно добавить запрос погоды через API
    });
});
