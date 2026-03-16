from flask import render_template, request, redirect, url_for, flash, send_file
from io import BytesIO
from datetime import datetime


def register_routes(app, service, repo):
    @app.route('/')
    def index():
        items = service.list_violations()
        return render_template('index.html', items=items)

    @app.route('/new', methods=['GET', 'POST'])
    def create():
        if request.method == 'POST':
            data = request.form
            service.create_violation(
                name=data.get('name', '').strip(),
                absen=data.get('absen', '').strip(),
                kelas=data.get('kelas', '').strip(),
                violation_type=data.get('violation_type', '').strip(),
                reason=data.get('reason', '').strip()
            )
            flash('Data berhasil ditambahkan', 'success')
            return redirect(url_for('index'))
        return render_template('form.html', item=None)

    @app.route('/view/<int:vid>')
    def view(vid):
        item = repo.get_by_id(vid)
        if not item:
            flash('Data tidak ditemukan', 'warning')
            return redirect(url_for('index'))
        return render_template('view.html', item=item)

    @app.route('/edit/<int:vid>', methods=['GET', 'POST'])
    def edit(vid):
        item = repo.get_by_id(vid)
        if not item:
            flash('Data tidak ditemukan', 'warning')
            return redirect(url_for('index'))
        if request.method == 'POST':
            data = request.form
            service.update_violation(vid,
                                     name=data.get('name', '').strip(),
                                     absen=data.get('absen', '').strip(),
                                     kelas=data.get('kelas', '').strip(),
                                     violation_type=data.get('violation_type', '').strip(),
                                     reason=data.get('reason', '').strip())
            flash('Data berhasil diperbarui', 'success')
            return redirect(url_for('index'))
        return render_template('form.html', item=item)

    @app.route('/delete/<int:vid>', methods=['POST'])
    def delete(vid):
        ok = service.delete_violation(vid)
        if ok:
            flash('Data berhasil dihapus', 'success')
        else:
            flash('Gagal menghapus data', 'danger')
        return redirect(url_for('index'))

    @app.route('/export', methods=['GET'])
    def export():
        try:
            csv_data = service.export_to_csv()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'violations_export_{timestamp}.csv'
            
            return send_file(
                BytesIO(csv_data.encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
        except Exception as e:
            flash(f'Gagal mengekspor data: {str(e)}', 'danger')
            return redirect(url_for('index'))

    @app.route('/import', methods=['GET', 'POST'])
    def import_data():
        if request.method == 'POST':
            try:
                if 'file' not in request.files:
                    flash('Tidak ada file yang dipilih', 'danger')
                    return redirect(url_for('import_data'))
                
                file = request.files['file']
                if file.filename == '':
                    flash('Tidak ada file yang dipilih', 'danger')
                    return redirect(url_for('import_data'))
                
                if not file.filename.endswith('.csv'):
                    flash('File harus berformat CSV', 'danger')
                    return redirect(url_for('import_data'))
                
                csv_content = file.read().decode('utf-8')
                success_count, error_count = service.import_from_csv(csv_content)
                
                flash(f'Impor berhasil: {success_count} data ditambahkan. Gagal: {error_count}', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Gagal mengimpor data: {str(e)}', 'danger')
                return redirect(url_for('import_data'))
        
        return render_template('import.html')
