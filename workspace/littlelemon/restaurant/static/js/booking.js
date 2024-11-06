console.log('booking.js loaded')

const date = new Date()
  document.getElementById('reservation_date').value = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate().toString().padStart(2, "0")}`

  getBookings()



  document.getElementById('reservation_date').addEventListener('change', function (e) {
    getBookings()
  })

  function getBookings() {
    let reserved_slots = []
    const date = document.getElementById('reservation_date').value
    document.getElementById('today').innerHTML = date
  
  
    fetch(bookingsUrl + '?date=' + date)
    .then(response => {
        // Log full response details
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        return response.text().then(text => {
            console.log('Raw response body:', text);
            
            try {
                return JSON.parse(text);
            } catch (e) {
                console.error('JSON parse error:', e);
                console.error('Response was:', text);
                throw new Error('Invalid JSON response');
            }
        });
    })
      .then(data => {
        reserved_slots = []
        bookings = ''
        
        
        for(let item of data){
          if (item.fields && item.fields.reservation_slot !== undefined) {
            const slot = Number(item.fields.reservation_slot)
            reserved_slots.push(slot)  
            bookings += `<p>${item.fields.first_name} - ${formatTime(slot)}</p>`
          } else {
            console.error('item.fields.reservation_slot is undefined for item:', item)
          }
        }
        
  
        /* Step 12: Part four */
        slot_options = '<option value="0" disabled>Select time</option>'
        for (let i = 10; i < 20; i++){
          const label = formatTime(i)
          if (reserved_slots.includes(i)) {
            slot_options += `<option value="${i}" disabled>${label}</option>`
          } else {
            slot_options += `<option value="${i}">${label}</option>`
          }
        }
        
  
        document.getElementById('reservation_slot').innerHTML = slot_options
        if(bookings == ''){
          document.getElementById('bookings').innerHTML = '<p>No Booking</p>'
        } else {
          document.getElementById('bookings').innerHTML = bookings
        }
      })
  }

  function formatTime(time) {
    const ampm = time < 12 ? 'AM' : 'PM'
    const t = time < 12 ? time : time > 12 ? time - 12 : time
    const label = `${t} ${ampm}`
    return label
  }


  document.getElementById('button').addEventListener('click', function (e) {
    const formdata = {
      first_name: document.getElementById('first_name').value,
      reservation_date: document.getElementById('reservation_date').value,
      reservation_slot: document.getElementById('reservation_slot').value,
    }

    fetch("{% url 'bookings' %}", { method: 'post', body: JSON.stringify(formdata) })
      .then(r => r.text())
      .then(data => {
        getBookings()
      })
  })