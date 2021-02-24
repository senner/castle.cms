/* global define */

define([
    'jquery',
    'underscore',
    'castle-url/libs/react/react.min',
    'castle-url/components/utils',
  ], function($, _, R, cutils) {

    'use strict';
    var D = R.DOM;

    var ContinuousContentComponent = cutils.Class([Modal], {
        getInitialState: function(){
            var data = JSON.parse($('body').attr('view-data'));
            return data
            debugger;
        },
        componentDidMount: function(){
            var that = this;
            window.onscroll = function(ev) {
                if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
                    that.loadBatch();
                }
            };
            this.renderBatch(this.state.firstBatch)
        },
        loadBatch: function(){
            this.setState({'batch': this.state.batch+1})
            // fetch context url ?b_start=
        },
        renderBatch: function(batchData){
            batchData.forEach(function(item){

            })
        },
        render: function() {
            
        }
    });

        var el = document.getElementById('continuous-content-div');
        R.render(R.createElement(ContinuousContentComponent), el);
    });
                