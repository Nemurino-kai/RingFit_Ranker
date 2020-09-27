<template>
  <div class="ranking container">
    <h2 >Exercise Ranking</h2> <div class="text-muted">({{start_day}} 04:00:00 ～ {{stop_day}} 03:59:59)</div>
    <hr style="margin-top:0.5em;margin-bottom:1em;">
    <form class="form-group form-inline">
      <label>集計日&nbsp;</label>
      <Datepicker v-model="defaultDate" :disabled-dates="disabledDates"></Datepicker>
    </form>

  <div class="overflow-auto" v-if="exercise_data.length != 0">
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="exercise-table"
      align="center"
    ></b-pagination>
      <b-table striped hover caption-top
      id="exercise-table"
          :items="exercise_data"
          :fields="columns"
          :per-page="perPage"
          :current-page="currentPage"
          small
    ></b-table>
        <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      @page-click="goTop"
      aria-controls="exercise-table"
      align="center"
    ></b-pagination>
    <p class="mt-3" style="text-align:center;">displaying <b>{{(currentPage-1)* 100 + 1}} - {{Math.min(currentPage* 100, exercise_data.length)}}</b> records in total <b>{{exercise_data.length}}</b></p>
  </div>

</div>
</template>

<script>
export default {
  data () {
    return {
      defaultDate: this.shiftDate(),
      disabledDates: {
        to: new Date(2020, 5 - 1, 18),
        from: this.shiftDate()
      },
      exercise_data: [],
      start_day: '',
      stop_day: '',
      currentPage: 1,
      perPage: 100,
      columns: [ {
        label: 'Rank',
        key: 'ranking',
        sortable: true
      },
      {
        label: 'Username',
        key: 'user_name',
        sortable: true
      },
      {
        label: 'kcal',
        key: 'kcal',
        sortable: true
      },
      {
        label: 'Date',
        key: 'tweeted_time',
        sortable: true
      }]
    }
  },
  methods: {
    // 4時間前の日付にシフトする
    shiftDate: function () {
      var shiftDate = new Date()
      shiftDate.setHours(shiftDate.getHours() - 4)
      return shiftDate
    },
    formatDate: function (date) {
      var d = new Date(date)
      var month = '' + (d.getMonth() + 1)
      var day = '' + d.getDate()
      var year = d.getFullYear()

      if (month.length < 2) { month = '0' + month }
      if (day.length < 2) { day = '0' + day }

      return [year, month, day].join('-')
    },
    goTop: function () {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    },
    readAPI: function (date) {
      var url = 'https://ringfit.work/api'
      if (typeof date !== 'undefined') {
        url = url + '?day=' + this.formatDate(date)
      }
      this.$store.commit('view/start')
      this.$api.get(url).then(res => {
        this.exercise_data = res['data']['exercise_data_list']
        this.start_day = res['data']['start_day']
        this.stop_day = res['data']['stop_day']
        this.$store.commit('view/end')
      })
    }
  },
  watch: {
    defaultDate: function (newDate) {
      this.readAPI(newDate)
    }
  },
  created () {
    this.readAPI()
  },
  computed: {
    rows () {
      return this.exercise_data.length
    }
  }
}
</script>
