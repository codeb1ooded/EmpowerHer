from flask import Flask, render_template
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config[ 'SECRET_KEY' ] = 'dklsfjsldjkfsdf'
socketio = SocketIO( app )
socketio.run(app, debug=True)


@app.route( '/' )
def index( self ):
	return render_template( './ChatAppPage.html' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
	print ('received something' + str( json ) )
	socketio.emit( 'my response', json )


