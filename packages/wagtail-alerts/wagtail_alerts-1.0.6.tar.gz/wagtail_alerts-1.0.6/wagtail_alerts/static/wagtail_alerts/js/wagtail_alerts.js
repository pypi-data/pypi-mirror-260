// https://stackoverflow.com/a/24103596/18020941
function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function eraseCookie(name) {   
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

// create alert component
class Alert extends HTMLElement {
    closeAlert() {
        const animation = [
            { height: this.offsetHeight + 'px', maxHeight: this.offsetHeight + 'px', fontSize: this.style.fontSize },
            { height: `0px`, maxHeight: `0px`, fontSize: '0em' }
        ];
        const animationConfig = {
            duration: 500,
            fill: 'forwards'
        };
        const anims = [
            this.animate(animation, animationConfig),
        ]
        for (let anim of anims) {
            anim.onfinish = () => {
                this.domDestroy();
            };
            anim.play();
        }
    }

    closeAlertClicked() {
        this.closeAlert();
        if (this.hasAttribute('data-permanent-dismiss') && this.hasAttribute('data-cookie-key')) {
            setCookie(this.dataset.cookieKey, 'true', 1);
        };
    }

    domSetup() {
        this.duration = this.dataset.duration || null;
        this.close = this.querySelector('.alert-dismissible');
        if (this.close) {
            this.close.addEventListener('click', this.closeAlertClicked.bind(this));
        }

        if (this.hasAttribute('data-once') && this.hasAttribute('data-cookie-key')) {
            // Use a timeout to prevent the alert from not being seen
            // if the page is refreshed too quickly.
            const cookieKey = this.dataset.cookieKey;
            setTimeout(() => {
                setCookie(cookieKey, 'true', 1);
            }, 3000);
        }
        
        if (this.duration && this.duration > 0) {
            let timer = setTimeout(() => {
                this.closeAlert();
            }, this.duration);
            this.addEventListener('mouseleave', () => {
                timer = setTimeout(() => {
                    this.closeAlert();
                }, this.duration);
            });
            this.addEventListener('mouseenter', () => {
                clearTimeout(timer);
            });
        }
    }

    domDestroy() {
        this.remove();
    }

    connectedCallback() {
        setTimeout(() => {
            this.domSetup();
        }, 0);
    }
}


class Toast extends Alert {

}


customElements.define('wagtail-alert', Alert);
customElements.define('wagtail-toast', Toast);