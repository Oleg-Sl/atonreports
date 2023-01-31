class FilterRange {
    constructor(container) {
        this.container = container;
        this.elemInputMin = this.container.querySelector('.filter-field-min-input');
        this.elemInputMax = this.container.querySelector('.filter-field-max-input');
        
    }

    init() {
        this.elemInputMin.addEventListener('change', async (e) => {
            this.checkMinValue();
        });
        this.elemInputMax.addEventListener('change', async (e) => {
            this.checkMaxValue();
        });
    }

    checkMinValue() {
        let min = this.elemInputMin.value;
        let max = this.elemInputMax.value;
        if (max && +min > +max) {
            this.elemInputMin.value = max;
        }
        if (+min < 0) {
            this.elemInputMin.value = 0;
        }
    }

    checkMaxValue() {
        let min = this.elemInputMin.value;
        let max = this.elemInputMax.value;
        if (min && +max < +min) {
            this.elemInputMax.value = min;
        }
        if (+max < 0) {
            this.elemInputMax.value = 0;
        }
    }

    getMinValue() {
        return this.elemInputMin.value;
    }

   
    getMaxValue() {
        return this.elemInputMax.value;
    }

}


export {FilterRange, };

