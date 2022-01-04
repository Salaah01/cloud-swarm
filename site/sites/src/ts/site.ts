import { BuildURL } from '../../../core_functions/ts/build_url';

interface WSResponseData {
  benchmark_id: number;
  status: string;
  num_servers: number;
  num_requests: number;
  completed_requests: number;
  failed_requests: number;
  created_on: string;
  scheduled_on: string | null;
  min_time: string | null;
  mean_time: string | null;
  max_time: string | null;
}

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
    const data = JSON.parse(event.data) as WSResponseData;
    console.log(data);

    const row = document.querySelector(
      `[data-benchmark-id="${data.benchmark_id}"]`
    );
    console.log(row);
    if (!row) return;
    updateRow(data);

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

  /**
   * Updates a row in the table with new data.
   * @param benchmarkID - The benchmark ID.
   * @param data - The data to update the row with.
   */
  const updateRow = (data: WSResponseData) => {
    const row = document.querySelector(
      `[data-benchmark-id="${data.benchmark_id}"]`
    ) as HTMLTableRowElement;

    // Created on
    row.querySelector(
      '[data-type="created-on"]'
    )!.textContent = data.created_on;

    // Scheduled on
    if (data.scheduled_on) {
      row.querySelector(
        '[data-type="scheduled-on"]'
      )!.textContent = data.scheduled_on;
    }

    // Status
    const statusInnerContainer = row.querySelector(
      '[data-type="status"] .benchmark-table__inner-container'
    ) as HTMLElement;
    statusInnerContainer.querySelector('span')!.textContent = data.status;
    if (data.status === 'Completed') {
      statusInnerContainer.querySelector('.spinner')?.remove();
    }

    // Number of servers
    row.querySelector(
      '[data-type="num-servers"]'
    )!.textContent = data.num_servers.toString();

    // Number of requests
    row.querySelector(
      '[data-type="num-requests"]'
    )!.textContent = data.num_requests.toString();

    // Min response time
    if (data.min_time && data.min_time != '0') {
      row.querySelector(
        '[data-type="min-time"]'
      )!.textContent = data.min_time;
    }

    // Mean response time
    if (data.mean_time && data.mean_time != '0') {
      row.querySelector(
        '[data-type="mean-time"]'
      )!.textContent = data.mean_time;
    }

    // Max response time
    if (data.max_time && data.max_time != '0') {
      row.querySelector(
        '[data-type="max-time"]'
      )!.textContent = data.max_time;
    }

    // Completed requests
    row.querySelector(
      '[data-type="completed-requests"]'
    )!.textContent = data.completed_requests.toString();

    // Failed requests
    row.querySelector(
      '[data-type="failed-requests"]'
    )!.textContent = data.failed_requests.toString();

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
