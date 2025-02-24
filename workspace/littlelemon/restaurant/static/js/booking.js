document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('booking_form');
    
    if (!form) {
        console.error('Booking form not found');
        return;
    }

    
    function initializeDateInput(takenSlots = []) {
        const dateInput = document.getElementById('booking_date');
        if (!dateInput) return;
        
        const today = new Date();
        dateInput.value = today.toISOString().split('T')[0];
        dateInput.addEventListener('change', getBookings);

      
        genTimeSlotOptions(takenSlots);
    }


    function genTimeSlotOptions(takenSlots = []) {
        const timeSlotSelect = document.getElementById('time_slot');
        if (!timeSlotSelect) return;
        
        timeSlotSelect.innerHTML = ''; 
        for (let i = 10; i < 21; i++) {
            const option = document.createElement('option');
            option.value = i;
            if (i < 12) {
                option.textContent = `${i}:00 AM`;
            } else {
                const hour = i > 12 ? i - 12 : i;
                option.textContent = `${hour}:00 PM`;
            }
            
            if (takenSlots.includes(i)) {
                option.disabled = true;
                option.style.color = 'grey';
            }
            
            timeSlotSelect.appendChild(option);
        }
    }

 
    function getBookings() {
        const dateInput = document.getElementById('booking_date');
        const today = document.getElementById('today');
        
        if (!dateInput || !today) return;
        
        today.innerHTML = dateInput.value;
        
        fetch(`${bookingsUrl}?date=${dateInput.value}`, {
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('data', data);
            
            const bookings = document.getElementById('bookings');
            if (!bookings) return;
            
            bookings.innerHTML = '';
            
            let takenSlots = [];
            if (Array.isArray(data)) {
                data.sort((a, b) => a.time_slot - b.time_slot)
                    .forEach(booking => {
                        if ('time_slot' in booking && 'name' in booking) { 
                            bookings.innerHTML += `<p>${booking.name} - ${booking.time_slot}:00</p>`;
                            takenSlots.push(booking.time_slot);
                        }
                    });
                if (data.length === 0) {
                    bookings.innerHTML = '<p>No bookings for this date</p>';
                } else {
                    genTimeSlotOptions(takenSlots);
                }
            } else {
                console.warn('Unexpected data structure:', data);
                bookings.innerHTML = '<p>No bookings found</p>';
            }
            
        })
        .catch(error => console.error('Error:', error));
    }

    const bookingsUrl = form.dataset.bookingsUrl;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = {
            name: document.getElementById('name').value,
            no_of_guests: parseInt(document.getElementById('no_of_guests').value),
            booking_date: document.getElementById('booking_date').value,
            time_slot: parseInt(document.getElementById('time_slot').value)
        };
        
        console.log("Form data being sent:", formData);

        fetch(bookingsUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.text().then(text => (text ? JSON.parse(text) : {})))
        .then(data => {
            console.log('Parsed response:', data);
            
            if (data.id) {
                getBookings();
                form.reset();
                initializeDateInput([]);
            }
            getBookings();
        })
        .catch(error => console.error('Error:', error));
    });

    const takenSlots = [];
    initializeDateInput(takenSlots);
    getBookings();
});
