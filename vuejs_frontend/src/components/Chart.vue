<script>
import { Bar } from 'vue-chartjs'
import { mapState } from 'vuex'
import zoom from 'chartjs-plugin-zoom'

export default {
  extends: Bar,
  name: 'chart',
  data () {
    return {
      data: {
        labels: [],
        titles: [],
        datasets: [
          {
            label: '消費カロリー',
            data: [],
            backgroundColor: 'rgba(255, 99, 132, 0.6)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            categoryPercentage: 1,
            barPercentage: 1
          }
        ]
      },
      options: {
        pan: {
          enabled: true,
          mode: 'x',
          rangeMin: {
            x: new Date('2020-05-17')
          },
          rangeMax: {
            x: new Date() - (1000 * 60 * 60 * 4)
          }
        },
        zoom: {
          enabled: true,
          mode: 'x',
          rangeMin: {
            x: new Date('2020-05-17')
          },
          rangeMax: {
            x: new Date() - (1000 * 60 * 60 * 4)
          }
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [{
            type: 'time',
            time: {
              displayFormats: {
                day: 'M/D'
              },
              unit: 'day'
            },
            scaleLabel: {
              display: true,
              labelString: 'Date'
            },
            ticks: {
              min: this.$moment().subtract(4, 'hours').subtract(30, 'days'),
              max: this.$moment().subtract(4, 'hours')
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true,
              stepSize: 100
            },
            scaleLabel: {
              display: true,
              labelString: 'kcal'
            }
          }]
        },
        tooltips: {
          callbacks:
    {
      title: function (array, data) {
        // labelの形式が RFC2822 or ISO format に従わないため、直接渡すとエラーがでる。そのため一旦Dateに変換する。
        return this.data.titles[array[0]['index']]
      }.bind(this)
    }
        }
      }
    }
  },
  computed: {
    ...mapState('userRank', ['exercise_data']),
    exerciseData: function () {
      return this.$store.state.userRank.exercise_data
    }
  },
  watch: {
    exerciseData () {
      this.$nextTick(() => {
        this.calculateChart()
        this.renderChart(this.data, this.options)
      })
    }
  },
  mounted () {
    this.addPlugin(zoom)
    this.renderChart(this.data, this.options)
  },
  created () {
    this.calculateChart()
  },
  methods: {
    calculateChart: function () {
      // ランキング算定時の日数に合わせるため、4時間引く
      this.data.labels = this.exercise_data.map(x => this.$moment(x['tweeted_time']).subtract(4, 'hours').format('YYYY-MM-DD'))
      this.data.titles = this.exercise_data.map(x => this.$moment(x['tweeted_time']).format('M/D A h:mm'))
      this.data.datasets[0].data = this.exercise_data.map(x => x['kcal'])
    },
    restoreDate: function (date) {
      // 実際の日時に戻すため、4時間足す
      return this.$moment(date).add(4, 'hours')
    }
  }

}
</script>
