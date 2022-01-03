import BuildURL from '../../../cloud_swarm/src/ts/utils/build_url';

/**
 * Calls out the verification check API to check if the site's DNS settings
 * include the correct TXT record. If the TXT record is missing, the user is
 * prompted to add it. If the TXT record is present, the page is reloaded.
 * @param id - The site ID.
 * @param slug - The site slug.
 */
const verificationCheck = (id: number, slug: string) => {
  const url = new BuildURL().siteVerificationCheckAPI(id, slug);
  fetch(url)
    .then(response => response.json())
    .then(json => {
      if (!json.success) {
        alert(json.message);
        return;
      }
      if (json.data.verified) {
        window.location.reload();
      } else {
        alert('Site is not verified');
      }
    })
};

/**Connects to a websocket which sends notifications regarding status changes
 * for certain benchmarks.
 * Update the page when a notification is received.
 */
const benchmarkProgress = () => {
  const siteID = (document.querySelector('#site-id') as HTMLElement).innerText;

  const ws = new WebSocket(
    `ws://${location.host}/ws/benchmark-progress/site/${siteID}/`
  );

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const statusInnerContainer = document.querySelector(
      `[data-benchmark-id="${data.benchmark_id}"] .benchmark-table__inner-container
    `) as HTMLElement;
    statusInnerContainer.querySelector('span')!.textContent = data.status;
    if (data.status === 'Completed') {
      statusInnerContainer.querySelector('.spinner')?.remove();
    }

  }

  ws.onclose = (_) => {
    console.error('WebSocket closed');
    const totalTries = 5;
    const interval = 1000;
    const retry = (tries: number) => {
      if (tries === totalTries) {
        console.error('Failed to reconnect to websocket');
        return;
      }
      setTimeout(() => {
        console.log('Attempting to reconnect to websocket');
        benchmarkProgress();
      }, interval);
    }
    retry(0);
  }
}

const main = () => {
  const verifyBtn = document.querySelector('#verify-btn') as HTMLButtonElement;
  const id = parseInt(verifyBtn.dataset.id as string, 10);
  const slug = verifyBtn.dataset.slug as string;
  verifyBtn.addEventListener('click', () => {
    verificationCheck(id, slug);
  });
  benchmarkProgress();
}

main();
