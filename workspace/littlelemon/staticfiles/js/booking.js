document.addEventListener('DOMContentLoaded', function() {
  
  const form = document.getElementById('booking_form');
  
  if (!form) {
      console.error('Booking form not found');
      return;
  }



  function initializeDateInput() {
      const dateInput = document.getElementById('booking_date');
      if (!dateInput) return;
      const today = new Date();
      dateInput.value = today.toISOString().split('T')[0];
      dateInput.addEventListener('change', getBookings);
  }

  function genTimeSlotOptions(takenSlots = []) {
    const timeSlotSelect = document.getElementById('time_slot');
    if (!timeSlotSelect) return;
    timeSlotSelect.innerHTML = ''; // Clear existing options
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
      const date = document.getElementById('booking_date')?.value;
      const today = document.getElementById('today');
      if (!date || !today) return;
      
      today.innerHTML = date;
      
      fetch(`${bookingsUrl}?date=${date}`, {
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
          const timeSlotSelect = document.querySelectorAll('option[name="time_slot"]');
          
          const takenSlots = [];
          data.sort((a, b) => a.fields['time_slot'] - b.fields['time_slot'])
          .forEach(booking => {
              bookings.innerHTML += `<p>${booking.fields['name']} - ${booking.fields['time_slot']}:00</p>`;
              takenSlots.push(booking.fields['time_slot']);
          });
          genTimeSlotOptions(takenSlots);
        }).then(() => {
          const bookings = document.getElementById('bookings');
          if (!bookings) return;
          if (bookings.innerHTML === '') {
              bookings.innerHTML = '<p>No bookings for this date</p>';
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
  .then(response => {
      console.log('Status:', response.status);
      return response.text().then(text => {
          console.log('Raw response:', text);
          return text ? JSON.parse(text) : {};
      });
  })
  .then(data => {
      console.log('Parsed response:', data);
      if (data.id) {
          getBookings();
          form.reset();
          initializeDateInput();
      }
  })
  .catch(error => console.error('Error:', error));
});

  // Initialize
  initializeDateInput();
  genTimeSlotOptions();
  getBookings();
});