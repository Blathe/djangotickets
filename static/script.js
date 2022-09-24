const detailsModal = document.getElementById('detailsModal')
detailsModal.addEventListener('show.bs.modal', event => {
      // Button that triggered the modal
      const button = event.relatedTarget

      // Extract info from data attributes
      const title = button.getAttribute('data-ticket-title')
      const description = button.getAttribute('data-ticket-description')
      const date = button.getAttribute('data-ticket-date')
      const owner = button.getAttribute('data-ticket-owner')
      const status = button.getAttribute('data-ticket-status')
      const priority = button.getAttribute('data-ticket-priority')


      //define all of our sections we need to edit
      const modalTitle = detailsModal.querySelector('.modal-title')
      const modalTitleEditable = detailsModal.querySelector('#edit-title')
      const modalPriority = detailsModal.querySelector('#edit-priority')
      const modalDescription = detailsModal.querySelector('#edit-description')
      const priorityBadge = detailsModal.querySelector('#priority-badge')
      const statusBadge = detailsModal.querySelector('#status-badge')
    
      //update our fields based on info extracted from data attributes
      modalTitle.textContent = title;
      modalTitleEditable.value = title;
      modalDescription.value = description;
      modalPriority.value = priority;

      //Clear our status badge info, then set our class names based on status
      statusBadge.className = "";
      statusBadge.textContent = status;

      switch (status){
        case 'OPEN':
            statusBadge.className = "badge bg-success";
            break;
        case 'CLOSED':
            statusBadge.className = "badge bg-danger"
            break;
        default:
            break;
      }

      //Clear our priority badge info, then set our class names based on priority
      priorityBadge.className = "";
      priorityBadge.textContent = priority;

      switch (priority){
        case 'HIGH':
            priorityBadge.className = "badge bg-danger text-dark";
            break;
        case 'MEDIUM':
            priorityBadge.className = "badge bg-warning text-dark";
            break;
        case 'LOW':
            priorityBadge.className = "badge bg-info text-dark";
            break;
        default:
            break;
      }
    })