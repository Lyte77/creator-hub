const revealElements = document.querySelectorAll(
    '.reveal-left, .reveal-scale, .reveal-item, .reveal-bottom'
  )

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed')
        observer.unobserve(entry.target)
      }
    })
  }, { threshold: 0.3 })

  revealElements.forEach(el => observer.observe(el))

  function handleCaptureState(textarea) {
    const form = textarea.closest('form');
    const label = form.querySelector('#capturing-label');
    const button = form.querySelector('#save-btn');

    if (textarea.value.trim().length > 0) {
      label.classList.remove('opacity-0');
      button.classList.remove('opacity-0', 'pointer-events-none', 'translate-y-1');
    } else {
      label.classList.add('opacity-0');
      button.classList.add('opacity-0', 'pointer-events-none', 'translate-y-1');
    }
  }

  function resetCaptureUI(form) {
    form.querySelector('#capturing-label')?.classList.add('opacity-0');
    form.querySelector('#save-btn')?.classList.add('opacity-0', 'pointer-events-none', 'translate-y-1');
  }