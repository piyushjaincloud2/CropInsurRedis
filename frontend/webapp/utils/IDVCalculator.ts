export const PREMIUM_RATE = 2
const LOW_QUALITY_ADJUSTMENT = 0.5

export const calculatePreHarvest = (data: any, preInspectionIDV, rate: number) => {
  const _Cultivatedland = parseFloat(`${data.CultivatedLand}`);
  let idv = preInspectionIDV * _Cultivatedland / 100;
  let premium = ((rate || PREMIUM_RATE) / 100) * idv;
  return { IDV: idv, premium }
}

export const calculatePostHarvest = (data: any, sumAssured) => {
  const _HighQualityCrop = parseFloat(data.HighQualityCrop)
  const _LowQualityCrop = parseFloat(data.LowQualityCrop)
  const _sum = parseFloat(sumAssured);
  let idv = (_sum * _HighQualityCrop / 100) +
    (_sum * _LowQualityCrop / 100) * LOW_QUALITY_ADJUSTMENT;
  return { IDV: (idv).toFixed(2) }
}

export const getBaseIDV = (data:any) => {
  const properties = data.properties[0];
  const baseIDV = parseFloat(properties.farmArea) * parseFloat(properties.expectedMarketPrice)*parseFloat(properties.expectedYeild)*100
  return (baseIDV).toFixed(2);
} 

export const getRecommanation = (avgValues) => {
  const recommendation = [];
  if(parseFloat(avgValues.humidity) < 14) {
    recommendation.push('The space between crops can be covered with a 2–3 inch layer of dry crop residues (natural mulch) to conserve soil moisture. Plastic mulch can be used to conserve moisture and to prevent weed growth.')
  }
  if(parseFloat(avgValues.moisture) > 90) {
    recommendation.push('Heavy rainfall expected.A traditional method to prevent water logging due to heavy rain is to dig deep trenches along the field length and fill it with large boulders or stones. This makes way for the water to flow out of the farm and reduce crop damage.')
  }
  if(parseFloat(avgValues.lowQualityCrop) > 0) {
    recommendation.push('Use fungicide spray during mid-season to reduce fungi wheat disease.On fertile soils, you can try using green manure. Pick forage legumes to grow (preventing weeds from emerging) and then turn into the soil to improve structure and act as manure.If you’ve already got good quality, nutritious soil (either through fertilising or crop rotation) don’t then overdo it with tilling. Leaving the soil as it is will encourage nutrient uptake in wheat.')
  }
  if(parseFloat(avgValues.temperature) > 35) {
    recommendation.push( ' Use a mulch to protect seedlings. If sprinkler irrigation is available, reduce high soil temperature during seedling emergence by irrigating at that time. Select the optimum sowing time, avoiding high temperature during anthesis and grain filling.')
  }
  if(parseFloat(avgValues.windSpeed) > 11) {
    recommendation.push('Cover your plants with overturned pots, bowls, buckets, or other appropriately-sized containers to keep them from suffering wind and rain damage. Be sure to weigh down the coverings in order to hold them in place–rocks, cement blocks, and bricks will work just fine')
  }
  if(avgValues?.weather?.toLowerCase() === 'rain') {
    recommendation.push('Cover your plants with overturned pots, bowls, buckets, or other appropriately-sized containers to keep them from suffering rain damage. Be sure to weigh down the coverings in order to hold them in place–rocks, cement blocks, and bricks will work just fine')
  }

  return recommendation.join('##');
}

export const averageFieldData = (data: any = []) => {
  const processData = data.reduce((acc = [], row: any) => {
    for (let key in row) {
      if (row[key] && !isNaN(row[key])) {
        if (!acc[key]) {
          acc[key] = 0;
        }
        acc[key] += parseFloat(row[key]);
      } else {
        if(row[key]) {
          acc[key] = row[key] 
        }
      }
    }
    return acc
  }, [])
  const len = data.length
  for (let key in processData) {
    if (processData[key] && !isNaN(processData[key])) {
      processData[key] = (processData[key] / len).toFixed(2);
    }
  }
  return processData
}