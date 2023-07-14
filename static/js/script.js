const animItems = document.querySelectorAll('._anim-items')

if (animItems.length > 0) {
    window.addEventListener('scroll', animOnScroll);
    function animOnScroll(params) {
        for (let index = 0; index < animItems.length; index++) {
            const animItem = animItems[index];
            const animItemHeight = animItem.offsetHeight;
            const animItemOffset = offset(animItem).top;
            const animStart = 4;

            let animItemPoint = window.innerHeight - animItemHeight / animStart;
            if (animItemHeight > window.innerHeight) {
                animItemPoint = window.innerHeight - window.innerHeight / animStart;
            }

            if ((scrollY > animItemOffset - animItemPoint) && scrollY < (animItemOffset + animItemHeight)) {
                animItem.classList.add('_active');

            } else {
                if (!animItem.classList.contains('_anim-no-hide')) {
                    animItem.classList.remove('_active');
                }
            }
        }
    }

    function offset(el) {
        const rect = el.getBoundingClientRect(),
            scrollLeft = scrollX || document.documentElement.scrollLeft,
            scrollTop = scrollY || document.documentElement.scrollTop;
        return { top: rect.top + scrollTop, left: rect.left + scrollLeft }
    }

    setTimeout(() => {
        animOnScroll();
    }, 300);
}


const close = document.getElementsByClassName('close');
const openBtn = document.getElementsByClassName('btn-open');

const btnDelete = document.querySelector('.btnDelete');

Array.from(close, closeButton => {
    closeButton.addEventListener('click', e => {
        e.target.closest('.modal').style.display = 'none'
    });
});

Array.from(openBtn, openButton => {
    openButton.addEventListener('click', e => {
        const modalType = e.target.getAttribute('data-type');
        const modal = document.getElementById(modalType);
        modal.style.display = 'flex';

        const dataArray = modal.querySelectorAll('.modal__input');
        const idInput = dataArray[0];
        const titleInput = dataArray[1];
        const startDateInput = dataArray[2];
        const endDateInput = dataArray[3];
        const textInput = modal.querySelector('textarea');

        window.addEventListener('click', (e) => {
            const target = e.target;
            if (!target.closest('.modal__content') && !target.closest('.btn-open')) {
                document.getElementById(modalType).style.display = 'none';
            }
        });

        modal.addEventListener('change', () => {
            formValidation(titleInput, startDateInput, endDateInput, modal);
        });

        if (modalType === 'modalEdit') {
            idInput.value = e.target.getAttribute('data-id');
            titleInput.value = e.target.getAttribute('data-title');
            textInput.value = e.target.getAttribute('data-text');
            startDateInput.value = dateFormat(e.target.getAttribute('data-startDate'));
            endDateInput.value = dateFormat(e.target.getAttribute('data-endDate'));
        }

        formValidation(titleInput, startDateInput, endDateInput, modal);
    });
});

function dateFormat(date) {
    let dateArray = date.split(' ');
    let time = dateArray[1];
    let timeArray = dateArray[0].split('.');
    const day = timeArray[0];
    const month = timeArray[1];
    const year = timeArray[2];

    return `${year}-${month}-${day}T${time}`;
};

function formValidation(title, startDate, endDate, modal) {
    if (title.value == '' || startDate.value == '' || endDate.value == ''
        || startDate.value > endDate.value) {
        modal.querySelector(".modalBtnAdd").setAttribute("disabled", "disabled");
    } else {
        modal.querySelector(".modalBtnAdd").removeAttribute("disabled");
    }
}