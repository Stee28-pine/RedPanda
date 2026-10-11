import { MOVIES } from "@consumet/extensions";

async function test(Provider) {
  try {
     const p = new Provider();
     const res = await p.search('Fight Club');
     console.log(Provider.name, 'OK', res.results[0].id);
  } catch (e) {
     console.log(Provider.name, 'FAIL', e.message);
  }
}
async function run() {
  await test(MOVIES.FlixHQ);
  await test(MOVIES.Dramacool);
  await test(MOVIES.Gojun);
  await test(MOVIES.KissAsian);
  await test(MOVIES.ViewAsian);
}
run();
