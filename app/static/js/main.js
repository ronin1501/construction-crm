console.log('Construction CRM loaded');

document.addEventListener('DOMContentLoaded', function () {
    const selects = document.querySelectorAll('select.form-select');

    function clearOpenCard(wrapper) {
        const card = wrapper.closest('.card');

        if (card) {
            card.classList.remove('custom-select-card-open');
        }
    }

    function setOpenCard(wrapper) {
        const card = wrapper.closest('.card');

        if (card) {
            card.classList.add('custom-select-card-open');
        }
    }

    function closeSelect(wrapper) {
        wrapper.classList.remove('open');
        clearOpenCard(wrapper);
    }

    selects.forEach(function (select) {
        if (select.dataset.customSelectReady === 'true') {
            return;
        }

        select.dataset.customSelectReady = 'true';
        select.classList.add('custom-select-original');

        const wrapper = document.createElement('div');
        wrapper.className = 'custom-select-wrapper';

        const trigger = document.createElement('div');
        trigger.className = 'custom-select-trigger';

        const optionsBox = document.createElement('div');
        optionsBox.className = 'custom-select-options';

        const selectedOption = select.options[select.selectedIndex];
        trigger.textContent = selectedOption
            ? selectedOption.textContent
            : 'Выберите значение';

        Array.from(select.options).forEach(function (option) {
            const customOption = document.createElement('div');
            customOption.className = 'custom-select-option';
            customOption.textContent = option.textContent;
            customOption.dataset.value = option.value;

            if (option.selected) {
                customOption.classList.add('selected');
            }

            customOption.addEventListener('click', function () {
                select.value = option.value;
                trigger.textContent = option.textContent;

                optionsBox
                    .querySelectorAll('.custom-select-option')
                    .forEach(function (item) {
                        item.classList.remove('selected');
                    });

                customOption.classList.add('selected');
                closeSelect(wrapper);

                select.dispatchEvent(new Event('change', { bubbles: true }));
            });

            optionsBox.appendChild(customOption);
        });

        trigger.addEventListener('click', function (event) {
            event.stopPropagation();

            document
                .querySelectorAll('.custom-select-wrapper.open')
                .forEach(function (item) {
                    if (item !== wrapper) {
                        closeSelect(item);
                    }
                });

            wrapper.classList.toggle('open');

            if (wrapper.classList.contains('open')) {
                setOpenCard(wrapper);
            } else {
                clearOpenCard(wrapper);
            }
        });

        wrapper.appendChild(trigger);
        wrapper.appendChild(optionsBox);

        select.parentNode.insertBefore(wrapper, select.nextSibling);
    });

    document.addEventListener('click', function () {
        document
            .querySelectorAll('.custom-select-wrapper.open')
            .forEach(function (item) {
                closeSelect(item);
            });
    });
});

// Автоматически добавляем адаптивную обертку ко всем таблицам
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("table.table").forEach(function (table) {
        if (table.parentElement.classList.contains("table-responsive-auto")) {
            return;
        }

        const wrapper = document.createElement("div");
        wrapper.className = "table-responsive-auto";

        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });
});
