<template>
  <div class="ranking container">
    <h2 >Exercise Ranking</h2> <div class="text-muted">({{exercise_data.start_day}} 04:00:00 ～ {{exercise_data.stop_day}} 03:59:59)</div>
    <hr style="margin-top:0.5em;margin-bottom:1em;">
    <form class="form-group form-inline">
      <label>集計日&nbsp;</label>
      <Datepicker v-model="defaultDate" :disabled-dates="disabledDates"></Datepicker>
    </form>

  <table class="table table-bordered" v-if="exercise_data.length != 0">
    <thead>
      <tr><th>Rank</th><th>Username</th><th>kcal</th><th>Date</th></tr>
    </thead>
    <tbody>
      <tr v-for="user in exercise_data['exercise_data_list']" :key="user.id">
        <td>{{user.ranking}}</td>
        <td>{{user.user_name}}</td>
        <td>{{user.kcal}}</td>
        <td>{{user.tweeted_time}}</td>
      </tr>
    </tbody>
  </table>  </div>
</template>

<script>

function formatDate (date) {
  var d = new Date(date)
  var month = '' + (d.getMonth() + 1)
  var day = '' + d.getDate()
  var year = d.getFullYear()

  if (month.length < 2) { month = '0' + month }
  if (day.length < 2) { day = '0' + day }

  return [year, month, day].join('-')
}

export default {
  data () {
    return {
      defaultDate: new Date(),
      disabledDates: {
        to: new Date(2020, 5 - 1, 18),
        from: new Date()
      },
      exercise_data: []
    }
  },
  watch: {
    defaultDate: function (newDate) {
      this.$api.get('https://ringfit.work/api?day=' + formatDate(newDate)).then(res => {
        this.exercise_data = res['data']
      })
    }
  },
  created () {
    this.$api.get('https://ringfit.work/api').then(res => {
      this.exercise_data = res['data']
    })
  }
}
</script>
