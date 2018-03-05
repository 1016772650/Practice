// 标尺类
function Rule(props) {
	this.x = props.x || 0;
	this.y = props.y || 0;	// 标尺的坐标位置
	this.vx = 0;			// 标尺的移动速度
	this.ax = 0;			// 标尺的移动加速度
	this.color = props.color || "#fff";		// 绘制标尺线条的颜色与文字颜色
	this.scaleX = props.scaleX || 1;
	this.scaleY = props.scaleY || 1;		// 缩放比
	this.markShort = -props.markShort || -5;
	this.markLong = -props.markLong || -10;		// 标尺长短线的长度
	this.textHeight = -props.textHeight || -5;	// 文字距离标尺主体的高度
	this.min = props.min || 1;					// 要展示的最大值和最小值，最大金额和最小金额
	this.max = props.max || 10000;
	this.width = props.width || 1000;			// 尺子的像素宽度
	this.step = props.step || 1000;				// 步长
	this.seg = Math.floor(this.max / this.step);	// 段数
	this.pxStep = Math.floor(this.width / this.seg);	// 每段在canvas上的实际宽度
	this.minPxStep = this.pxStep / 10;					// 每个刻度在canvas上的实际像素距离
	this.ratioScale = Math.floor(this.max / this.width);	// 比例尺
	// 底部横线参数
	this.lineBottom = Object.assign(
		{}, 
		{
			mx: null,
			my: null,
			lx: null,
			ly: null,
			color: '#fff'
		},
		props.lineBottom || {}
	);
	// 标定轴参数
	this.lineRed = Object.assign(
		{},
		{
			mx: 0,
			my: 0,
			lx: 0,
			ly: 5,
			color: 'red',
			isDrawRedLine: true
		},
		props.lineRed || {}
	);
	
}

Rule.prototype.draw = function(ctx) {
	var n = 0;
	ctx.save();
	ctx.translate(this.x, this.y);
	ctx.lineWidth = 1
	ctx.scale(this.scaleX, this.scaleY);
	ctx.fillStyle = this.color;
	ctx.strokeStyle = this.color;
	ctx.textAlign = "center";
	ctx.beginPath();
	for(var i=0; i<=this.width; i+=this.minPxStep) {
		ctx.moveTo(i, 0);
		if (n % 10 === 0) {
			ctx.lineTo(i, this.markLong);
			if (i === 0) {
				ctx.fillText(1, i, this.markLong + this.textHeight);
			} else {
				ctx.fillText(n/10*this.step, i, this.markLong + this.textHeight);
			}
		} else {
			ctx.lineTo(i, this.markShort);
		}
		n++;
	}
	
	ctx.closePath();
	ctx.stroke();
	ctx.restore();
	
	// 底部横线参数
	ctx.save();
	ctx.strokeStyle = this.lineBottom.color;
	ctx.scale(this.scaleX, this.scaleY);
	ctx.beginPath();
	ctx.moveTo(this.lineBottom.mx, this.lineBottom.my);
	ctx.lineTo(this.lineBottom.lx, this.lineBottom.ly);
	ctx.stroke();
	ctx.closePath();
	ctx.restore();
	
	
	//中心线
	if (this.lineRed.isDrawRedLine) {
		ctx.save();
		ctx.strokeStyle = this.lineRed.color;
		ctx.lineWidth = 1;
		ctx.scale(this.scaleX, this.scaleY);
		ctx.beginPath();
		ctx.moveTo(this.lineRed.mx, this.lineRed.my);
		ctx.lineTo(this.lineRed.lx, this.lineRed.ly);
		ctx.stroke();
		ctx.closePath();
		ctx.restore();
	}
}

