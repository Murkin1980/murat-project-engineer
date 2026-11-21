/* Offline only. Pass the pinned local furniture-orders-mvp checkout. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
const repo = resolve(process.argv[2]);
assert.equal(execFileSync('git',['-C',repo,'rev-parse','HEAD'],{encoding:'utf8'}).trim(),'546eb359314af5199b88d985a994b66507af84b5');
const {estimateCalculatorPrice} = await import(pathToFileURL(resolve(repo,'src/calculators-pricing.js')));
const key = JSON.parse(readFileSync(new URL('review-key.json',import.meta.url)));
const csv = new URL('commercial-review.csv',import.meta.url);
const rows = JSON.parse(execFileSync('python3',['-c','import csv,json,sys;print(json.dumps(list(csv.DictReader(open(sys.argv[1])))))',decodeURIComponent(csv.pathname)]));
assert.equal(rows.length,50);
let checked = 0;
for(const row of rows){
  const ref = key[row.id];
  assert.equal(row.approved_total_kzt,'');
  if(ref.action !== 'estimate') continue;
  const unitPrices = ref.product === 'kitchen' ? [159500,205000,247500,319000] : [75000,90000,95000,110000];
  for(const [index,field] of ['ldsp_ru','egger','mdf_film','mdf_paint'].entries()){
    assert.equal(estimateCalculatorPrice({minUnits:1,unitPrice:unitPrices[index]},Number(ref.quantity)),Number(row[field+'_subtotal']));
    checked++;
  }
}
assert.equal(checked,128);
console.log('PASS: 50 IDs; 128 conditional base subtotals; zero approved totals');
