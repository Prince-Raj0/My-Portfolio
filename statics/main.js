var typed = new Typed(".text", {
    strings: ["Frontend Developer", "Backend Developer", "Full Stack Developer", "UI/UX Designer", "Web Application Developer", "Database Manager", "Python Flask Developer"],

    typeSpeed: 100,
    backSpeed: 100,
    backDelay: 1000,
    loop: true
});

document.addEventListener('DOMContentLoaded', () => {
    // Animate technical skill bars
    document.querySelectorAll('.progress-line').forEach(line => {
        const percentText = line.querySelector('.percentage').textContent.trim();
        const percent = parseInt(percentText.replace('%', ''));
        line.style.setProperty('--progress', percent + '%');

        // Trigger animation
        setTimeout(() => {
            line.classList.add('animate');
        }, 100);
    });

    // Animate radial progress
    document.querySelectorAll('.path').forEach(circle => {
        const percent = circle.getAttribute('data-percent');
        const radius = circle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (percent / 100) * circumference;

        circle.style.strokeDasharray = `${circumference}`;
        circle.style.strokeDashoffset = `${circumference}`;

        setTimeout(() => {
            circle.style.strokeDashoffset = offset;
        }, 500);
    });
});
