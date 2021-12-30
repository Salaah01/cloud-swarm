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
  console.log(id, slug)
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

const main = () => {
  const verifyBtn = document.querySelector('#verify-btn') as HTMLButtonElement;
  const id = parseInt(verifyBtn.dataset.id as string, 10);
  const slug = verifyBtn.dataset.slug as string;
  verifyBtn.addEventListener('click', () => {
    verificationCheck(id, slug);
  });
}

main();
